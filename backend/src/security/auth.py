from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from src.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRES_MINUTES
from src.models.users import UserDocument
from src.dal.users import UsersDAL
from src.utils.logger import logger


oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='/api/auth/login')


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=JWT_EXPIRES_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {'sub': subject, 'exp': expire}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDocument:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: str | None = payload.get('sub')
        if user_id is None:
            logger.warning('JWT token missing subject (sub) claim')
            raise credentials_exception
    except JWTError as e:
        logger.warning(f'JWT validation failed: {str(e)}')
        raise credentials_exception

    users_dal = UsersDAL()
    user = await users_dal.get_user_by_id(user_id)
    if user is None:
        logger.warning(f'User not found for authenticated token: user_id={user_id}')
        raise credentials_exception

    return user
