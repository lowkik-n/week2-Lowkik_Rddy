from enum import Enum
from typing import Callable

from fastapi import Depends, HTTPException, status

from product.models.user import User
from product.utils.security import get_current_user


class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    SUPPORT = "support"


def require_roles(
    *allowed_roles: str,
) -> Callable:
    allowed_role_set = set(allowed_roles)

    def role_dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        current_role = (current_user.Role or "").lower()

        if current_role not in allowed_role_set:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role permissions",
            )

        return current_user

    return role_dependency


def ensure_user_access(
    requested_user_id: int,
    current_user: User,
    allowed_roles: tuple[str, ...] = (
        UserRole.ADMIN.value,
    ),
) -> None:
    current_role = (current_user.Role or "").lower()

    is_owner = current_user.UserID == requested_user_id
    has_override_role = current_role in set(allowed_roles)

    if not is_owner and not has_override_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can access only your own resources",
        )
