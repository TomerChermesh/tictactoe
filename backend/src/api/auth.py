from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

from pymongo.errors import DuplicateKeyError

from src.models.auth import LoginRequest, LoginResponse, LogoutResponse
from src.models.users import UserDocument
from src.dal.users import UsersDAL
from src.dependencies import get_users_dal
from src.security.password import hash_password, verify_password
from src.security.auth import create_access_token, get_current_user


router: APIRouter = APIRouter(prefix='/auth')


@router.post('/register', response_model=LoginResponse)
async def register(
    payload: LoginRequest,
    users_dal: UsersDAL = Depends(get_users_dal)
):
    try:
        password_hash: str = hash_password(payload.password)
        user: UserDocument = await users_dal.create_user(payload.email, password_hash)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail='User with this email already exists'
        )
    
    access_token: str = create_access_token(subject=str(user.id))

    return LoginResponse(
        ok=True,
        user=user,
        accessToken=access_token,
        tokenType='bearer'
    )


@router.post('/login', response_model=LoginResponse)
async def login(
    payload: LoginRequest,
    users_dal: UsersDAL = Depends(get_users_dal)
):
    user: Optional[UserDocument] = await users_dal.get_user_by_email(payload.email)

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=401,
            detail='Invalid email or password'
        )

    access_token: str = create_access_token(subject=str(user.id))

    return LoginResponse(
        ok=True,
        user=user,
        accessToken=access_token,
        tokenType='bearer'
    )

@router.post('/logout', response_model=LogoutResponse)
async def logout(
    current_user: UserDocument = Depends(get_current_user)
):
    return LogoutResponse(
        ok=True,
        message='Logged out successfully'
    )   