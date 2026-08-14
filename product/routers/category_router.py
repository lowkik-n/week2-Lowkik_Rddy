from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.schemas.category_schema import CategoryCreate, CategoryResponse
from product.services import category_service
from product.models.user import User
from product.utils.security import get_current_user
from product.utils.authorization import UserRole, require_roles

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=201,
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN.value),
    ),
):
    try:
        return category_service.create_category(
            db=db,
            category_data=category,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.get(
    "",
    response_model=list[CategoryResponse],
)
def get_categories(
    db: Session = Depends(get_db),
):
    return category_service.get_all_categories(db)
