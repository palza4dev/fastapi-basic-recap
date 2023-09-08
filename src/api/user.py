from fastapi import APIRouter, Depends

from database.orm import User
from database.repository import UserRepository
from schema.request import SignUpRequest
from schema.response import UserSchema
from service.user import UserService

router = APIRouter(prefix="/users")


@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(),
        user_repository: UserRepository = Depends()
):
    hashed_password: str = user_service.hash_password(
        plain_password=request.password
    )
    user: User = User.create(
        username=request.username, hashed_password=hashed_password
    )  # id=None
    user: User = user_repository.save_user(user=user)  # id=int
    return UserSchema.from_orm(user)
