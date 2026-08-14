import os
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.models.user import User
from product.utils.logger import logger


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "development-only-secret-change-this",
)

ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
)


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_context.verify(
        plain_password,
        hashed_password,
    )


def generate_token(data: dict[str, Any]) -> str:
    payload = data.copy()

    payload["exp"] = datetime.now(
        timezone.utc,
    ) + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES,
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        subject = payload.get("sub")

        if not subject:
            raise credentials_exception

        user_id = int(subject)

    except (JWTError, ValueError) as error:
        logger.warning(
            "JWT validation failed: %s",
            str(error),
        )
        raise credentials_exception from error

    user = db.get(User, user_id)

    if user is None:
        logger.warning(
            "JWT references missing user_id=%s",
            user_id,
        )
        raise credentials_exception

    logger.info(
        "Authenticated request for user_id=%s",
        user.UserID,
    )

    return user

def require_roles(*allowed_roles: str):
    normalized_roles = {
        role.strip().lower()
        for role in allowed_roles
    }

    def role_dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        current_role = (current_user.Role or "").strip().lower()

        if current_role not in normalized_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role permissions",
            )

        return current_user

    return role_dependency
