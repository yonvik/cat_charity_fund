from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_register_router(
        user_schema=UserRead, user_create_schema=UserCreate
    ),
    prefix="/auth",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_users_router(
        user_schema=UserRead, user_update_schema=UserUpdate
    ),
    prefix="/users",
    tags=["Users"],
)


@router.delete("/users/{id}", tags=["Users"], deprecated=True)
def delete_user(id: str):
    raise HTTPException(
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail="Удаление пользователей запрещено!",
    )
