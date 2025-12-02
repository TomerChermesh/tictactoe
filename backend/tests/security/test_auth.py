import pytest
from datetime import datetime, timedelta, timezone
from typing import Dict
from unittest.mock import Mock, patch, AsyncMock
from jose import jwt, JWTError
from fastapi import HTTPException, status
from src.security.auth import create_access_token, get_current_user
from src.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRES_MINUTES
from src.models.users import UserDocument


class TestCreateAccessToken:   
    @pytest.mark.parametrize('subject, expires_delta, expected_result', [
        ('user123', None, True),
        ('user123', timedelta(minutes=30), True),
        ('user1', None, True),
        ('user2', None, True),
        ('user123', timedelta(seconds=0), True),
        ('user123', timedelta(days=365), True),
    ], ids=['default_expiry', 'custom_expiry', 'subject1', 'subject2', 'zero_expiry', 'long_expiry'])
    def test_create_access_token(self, subject: str, expires_delta: timedelta | None, expected_result: bool) -> None:
        token: str = create_access_token(subject, expires_delta=expires_delta)
        assert isinstance(token, str) == expected_result
        assert len(token) > 0
        payload: Dict[str, str | int] = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        assert payload['sub'] == subject
        if expires_delta is not None:
            exp_time: datetime = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)
            expected_time: datetime = datetime.now(timezone.utc) + expires_delta
            time_diff: float = abs((exp_time - expected_time).total_seconds())
            assert time_diff < 60


class TestGetCurrentUser:    
    @pytest.mark.parametrize('user_id, token_type, user_exists, expected_status_code', [
        ('507f1f77bcf86cd799439011', 'valid', True, None),
        ('507f1f77bcf86cd799439011', 'invalid', False, status.HTTP_401_UNAUTHORIZED),
        ('507f1f77bcf86cd799439011', 'expired', False, status.HTTP_401_UNAUTHORIZED),
        ('507f1f77bcf86cd799439011', 'missing_sub', False, status.HTTP_401_UNAUTHORIZED),
        ('507f1f77bcf86cd799439011', 'valid', False, status.HTTP_401_UNAUTHORIZED),
        ('507f1f77bcf86cd799439011', 'wrong_secret', False, status.HTTP_401_UNAUTHORIZED),
        ('', 'valid', False, status.HTTP_401_UNAUTHORIZED),
        ('507f1f77bcf86cd799439011', 'malformed', False, status.HTTP_401_UNAUTHORIZED),
    ], ids=['valid', 'invalid_format', 'expired', 'missing_sub', 'nonexistent_user', 'wrong_secret', 'empty_subject', 'malformed'])
    @pytest.mark.asyncio
    async def test_get_current_user(self, user_id: str, token_type: str, user_exists: bool, expected_status_code: int | None) -> None:
        if token_type == 'valid':
            token: str = create_access_token(user_id)
        elif token_type == 'invalid':
            token = 'invalid_token_string'
        elif token_type == 'expired':
            expire: datetime = datetime.now(timezone.utc) - timedelta(hours=1)
            to_encode: Dict[str, str | datetime] = {'sub': user_id, 'exp': expire}
            token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        elif token_type == 'missing_sub':
            expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRES_MINUTES)
            to_encode = {'exp': expire}
            token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        elif token_type == 'wrong_secret':
            wrong_secret: str = 'wrong_secret_key'
            expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRES_MINUTES)
            to_encode = {'sub': user_id, 'exp': expire}
            token = jwt.encode(to_encode, wrong_secret, algorithm=JWT_ALGORITHM)
        elif token_type == 'malformed':
            token = 'not.a.valid.jwt.token'
        else:
            token = create_access_token(user_id)
        
        if expected_status_code is None:
            mock_user: Mock = Mock(spec=UserDocument)
            mock_user.id = user_id
            with patch('src.security.auth.UsersDAL') as mock_dal_class:
                mock_dal: Mock = Mock()
                mock_dal.get_user_by_id = AsyncMock(return_value=mock_user)
                mock_dal_class.return_value = mock_dal
                result: UserDocument = await get_current_user(token)
                assert result == mock_user
                mock_dal.get_user_by_id.assert_called_once_with(user_id)
        else:
            with patch('src.security.auth.UsersDAL') as mock_dal_class:
                mock_dal = Mock()
                mock_dal.get_user_by_id = AsyncMock(return_value=None if not user_exists else Mock(spec=UserDocument))
                mock_dal_class.return_value = mock_dal
                with pytest.raises(HTTPException) as exc_info:
                    await get_current_user(token)
                assert exc_info.value.status_code == expected_status_code
