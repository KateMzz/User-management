from unittest.mock import AsyncMock

import pytest
from jose import ExpiredSignatureError, JWTError, jwt

from settings import settings
from src.services.auth.auth_service import AuthService
from utils.error_handler import UserNotFound


async def test_auth_user_success(common_auth_patches, mock_session, username, password):
    mock_get_user, mock_verify_password, mock_get_tokens = common_auth_patches
    mock_get_user.return_value = AsyncMock()
    mock_verify_password.return_value = True
    mock_get_tokens.return_value = ("access_token", "refresh_token")
    result = await AuthService(mock_session).authenticate_user(username, password)
    assert result == ("access_token", "refresh_token")


async def test_auth_user_user_not_found(common_auth_patches, mock_session, username, password):
    mock_get_user, mock_verify_password, mock_get_tokens = common_auth_patches
    mock_get_user.return_value = None
    result = await AuthService(mock_session).authenticate_user(username, password)
    assert result is False


async def test_authenticate_user_password_mismatch(
    common_auth_patches, mock_session, username, password
):
    mock_get_user, mock_verify_password, mock_get_tokens = common_auth_patches
    mock_get_user.return_value = AsyncMock()
    mock_verify_password.return_value = False
    result = await AuthService(mock_session).authenticate_user(username, password)
    assert result is False


async def test_generate_token_success(mock_session, test_user_id):
    encoded_token = await AuthService(mock_session).generate_token(user_id=test_user_id, days=2)
    decoded_payload = jwt.decode(
        encoded_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert decoded_payload["user_id"] == test_user_id


async def test_generate_token_exp(mock_session, test_user_id):
    encoded_token = await AuthService(mock_session).generate_token(user_id=test_user_id, days=-1)
    with pytest.raises(ExpiredSignatureError):
        jwt.decode(encoded_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


async def test_generate_access_token_success(mock_session, test_user_id):
    encoded_token = await AuthService(mock_session).generate_access_token(user_id=test_user_id)
    decoded_payload = jwt.decode(
        encoded_token.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert encoded_token.token is not None
    assert decoded_payload["user_id"] == test_user_id


async def test_generate_access_token_fail(mock_session):
    with pytest.raises(UserNotFound):
        await AuthService(mock_session).generate_access_token(user_id=None)


async def test_get_user_id_from_token(mock_session, exp_token, test_user_id):
    user_id = await AuthService(mock_session).get_user_id_from_token(exp_token)
    assert user_id == test_user_id


async def test_get_user_id_from_token_fail(mock_session):
    with pytest.raises(JWTError):
        await AuthService(mock_session).get_user_id_from_token(AsyncMock())


async def test_get_access_refresh_tokens(mock_session, test_user_id):
    result = await AuthService(mock_session).get_access_refresh_tokens(user_id=test_user_id)
    assert result.access_token and result.refresh_token
    access_user_id = jwt.decode(
        result.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )["user_id"]
    refresh_user_id = jwt.decode(
        result.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )["user_id"]
    assert access_user_id == refresh_user_id == test_user_id


async def test_get_access_refresh_tokens_fail(mock_session, test_user_id):
    with pytest.raises(UserNotFound):
        await AuthService(mock_session).get_access_refresh_tokens(user_id=None)


async def test_blacklist_token(mock_session, mock_redis, exp_token, test_user_id):
    mock_redis.smembers.return_value = set()
    result = await AuthService(mock_session).blacklist_token(exp_token, mock_redis, test_user_id)
    assert result is True
    mock_redis.sadd.assert_called_once_with(test_user_id, exp_token)


async def test_blacklist_token_fail(mock_session, mock_redis, exp_token, test_user_id):
    mock_redis.smembers.return_value = {exp_token}
    result = await AuthService(mock_session).blacklist_token(exp_token, mock_redis, test_user_id)
    assert result is False
    mock_redis.sadd.assert_not_called()


async def test_blacklist_token_multiple_tokens(mock_session, mock_redis, exp_token, test_user_id):
    existing_tokens = {"existing_token_1", "existing_token_2"}
    mock_redis.smembers.return_value = existing_tokens
    result = await AuthService(mock_session).blacklist_token(exp_token, mock_redis, test_user_id)
    assert result is True
    mock_redis.sadd.assert_called_once_with(test_user_id, exp_token)
