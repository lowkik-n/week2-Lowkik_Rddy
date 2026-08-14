from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.repositories import user_repository
from product.schemas.user_schema import TokenResponse
from product.utils.logger import logger
from product.utils.security import (
    generate_token,
    verify_password,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    email = form_data.username.strip().lower()

    user = user_repository.get_user_by_email(
        db,
        email,
    )

    if user is None or not verify_password(
        form_data.password,
        user.Password,
    ):
        logger.warning(
            "Failed login attempt for email=%s",
            email,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = generate_token(
        {
            "sub": str(user.UserID),
        },
    )

    logger.info(
        "Successful login for user_id=%s",
        user.UserID,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
