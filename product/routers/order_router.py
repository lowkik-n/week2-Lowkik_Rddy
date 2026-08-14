from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.models.user import User
from product.schemas.order_schema import (
    OrderCreate,
    OrderHistoryResponse,
    OrderResponse,
)
from product.services import order_service
from product.utils.security import get_current_user


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


PRIVILEGED_ORDER_ROLES = {"admin", "support"}


def get_user_role(user: User) -> str:
    """Return the user's role in normalized lowercase form."""
    return str(user.Role).strip().lower()


def service_error_to_http(error: ValueError) -> HTTPException:
    """Convert business validation errors into HTTP responses."""
    message = str(error)
    message_lower = message.lower()

    if (
        "not found" in message_lower
        or "no longer exists" in message_lower
    ):
        error_status = status.HTTP_404_NOT_FOUND
    elif "stock" in message_lower:
        error_status = status.HTTP_409_CONFLICT
    else:
        error_status = status.HTTP_400_BAD_REQUEST

    return HTTPException(
        status_code=error_status,
        detail=message,
    )


def ensure_order_access(order, current_user: User) -> None:
    """Allow owners, admins, and support users to access an order."""
    is_owner = order.UserID == current_user.UserID
    is_privileged = (
        get_user_role(current_user) in PRIVILEGED_ORDER_ROLES
    )

    if not is_owner and not is_privileged:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access this order",
        )


@router.post(
    "/checkout",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def checkout(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Place an order for the authenticated customer."""
    if get_user_role(current_user) != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can place orders",
        )

    # Never trust the user_id supplied by the client.
    secured_order_data = order_data.model_copy(
        update={"user_id": current_user.UserID},
    )

    try:
        return order_service.create_order(
            db,
            secured_order_data,
        )
    except ValueError as error:
        raise service_error_to_http(error) from error
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to place the order",
        ) from error


@router.get(
    "/me",
    response_model=list[OrderHistoryResponse],
)
def get_my_order_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return orders belonging to the authenticated user."""
    try:
        return order_service.get_orders_by_user(
            db,
            current_user.UserID,
        )
    except ValueError as error:
        raise service_error_to_http(error) from error


@router.get(
    "/details/{order_id}",
    response_model=OrderResponse,
)
def get_order_details(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return order details after ownership or role validation."""
    order = order_service.get_order_by_id(
        db,
        order_id,
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    ensure_order_access(order, current_user)

    return order


@router.get(
    "/{user_id}",
    response_model=list[OrderHistoryResponse],
)
def get_order_history(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return order history for the requested user.

    Customers can request only their own history.
    Admin and support users can request any user's history.
    """
    is_owner = user_id == current_user.UserID
    is_privileged = (
        get_user_role(current_user) in PRIVILEGED_ORDER_ROLES
    )

    if not is_owner and not is_privileged:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can view only your own order history",
        )

    try:
        return order_service.get_orders_by_user(
            db,
            user_id,
        )
    except ValueError as error:
        raise service_error_to_http(error) from error
