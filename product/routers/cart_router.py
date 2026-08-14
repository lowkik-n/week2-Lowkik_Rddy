from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.models.user import User
from product.schemas.cart_schema import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
    CartSummary,
)
from product.services import cart_service
from product.utils.security import get_current_user
from product.repositories import cart_repository
from product.utils.authorization import ensure_user_access
from product.utils.security import get_current_user


router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


def raise_cart_error(error: ValueError) -> None:
    detail = str(error)

    not_found_messages = {
        "User not found",
        "Product not found",
        "Cart item not found",
        "Product in cart no longer exists",
    }

    if detail in not_found_messages:
        error_status = status.HTTP_404_NOT_FOUND

    elif detail == "Cart item does not belong to this user":
        error_status = status.HTTP_403_FORBIDDEN

    elif "stock" in detail.lower():
        error_status = status.HTTP_409_CONFLICT

    else:
        error_status = status.HTTP_400_BAD_REQUEST

    raise HTTPException(
        status_code=error_status,
        detail=detail,
    )


@router.post(
    "/add",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_user_access(
        requested_user_id=item.user_id,
        current_user=current_user,
        allowed_roles=(),
    )

    try:
        return cart_service.add_to_cart(
            db=db,
            item_data=item,
        )
    except ValueError as error:
        raise_cart_error(error)




@router.get(
    "/{user_id}",
    response_model=list[CartItemResponse],
)
def get_cart(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_user_access(
        requested_user_id=user_id,
        current_user=current_user,
        allowed_roles=(),
    )

    try:
        return cart_service.get_cart(
            db=db,
            user_id=user_id,
        )
    except ValueError as error:
        raise_cart_error(error)

@router.get(
    "/{user_id}/summary",
    response_model=CartSummary,
)
def get_cart_summary(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_user_access(
        requested_user_id=user_id,
        current_user=current_user,
        allowed_roles=(),
    )

    try:
        return cart_service.get_cart_summary(
            db=db,
            user_id=user_id,
        )
    except ValueError as error:
        raise_cart_error(error)


@router.put(
    "/update/{cart_item_id}",
    response_model=CartItemResponse,
)
def update_cart_item(
    cart_item_id: int,
    item: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_item = cart_repository.get_cart_item_by_id(
        db,
        cart_item_id,
    )

    if cart_item is not None:
        ensure_user_access(
            requested_user_id=cart_item.UserID,
            current_user=current_user,
            allowed_roles=(),
        )

    try:
        return cart_service.update_cart_item(
            db=db,
            cart_item_id=cart_item_id,
            item_data=item,
        )
    except ValueError as error:
        raise_cart_error(error)


@router.delete(
    "/remove/{cart_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_item = cart_repository.get_cart_item_by_id(
        db,
        cart_item_id,
    )

    if cart_item is not None:
        ensure_user_access(
            requested_user_id=cart_item.UserID,
            current_user=current_user,
            allowed_roles=(),
        )

    try:
        cart_service.remove_cart_item(
            db=db,
            cart_item_id=cart_item_id,
        )
    except ValueError as error:
        raise_cart_error(error)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
