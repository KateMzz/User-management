from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from src.schemas.sch_user import UserDetailUpdate
from src.services.auth.user_service import UserService
from src.tests.factories import UserFactoryNoHash
from utils.error_handler import UserCreateError


@patch("src.services.auth.auth_service.AuthService.get_password_hash", return_value=AsyncMock())
@patch("src.repositories.repo_user.UserRepository.create_user", return_value="user")
async def test_create_user_with_hashedpass(mock_user, get_password_hash, mock_session):
    user = UserFactoryNoHash()
    result = await UserService(mock_session).create_user_with_hashedpass(user=user)
    assert result == mock_user.return_value
    get_password_hash.assert_called_once_with(password=user.password)


@patch("src.services.auth.auth_service.AuthService.get_password_hash", return_value=None)
async def test_create_user_with_hashedpass_fail(get_password_hash, mock_session):
    user = UserFactoryNoHash()
    with pytest.raises(UserCreateError):
        await UserService(mock_session).create_user_with_hashedpass(user=user)
    get_password_hash.assert_called_once_with(password=user.password)


@patch(
    "src.services.auth.auth_service.AuthService.get_user_id_from_token", return_value=AsyncMock()
)
@patch("src.repositories.repo_user.UserRepository.get_user_by_id", return_value="user")
async def test_get_current_user(mock_user_by_id, mock_user_id_from_token, mock_session, exp_token):
    result = await UserService(mock_session).get_current_user(exp_token)
    assert result == mock_user_by_id.return_value
    mock_user_id_from_token.assert_called_once_with(token=exp_token)


@patch(
    "src.services.auth.auth_service.AuthService.get_user_id_from_token", return_value=AsyncMock()
)
@patch("src.repositories.repo_user.UserRepository.get_user_by_id", return_value=None)
async def test_get_current_user_fail(
    mock_user_by_id, mock_user_id_from_token, mock_session, exp_token
):
    with pytest.raises(HTTPException):
        result = await UserService(mock_session).get_current_user(exp_token)
        assert "Wrong credentials" in result
    mock_user_id_from_token.assert_called_once_with(token=exp_token)


@patch("src.services.auth.user_service.UserRepository.update_user")
@patch("src.services.auth.user_service.UserRepository.row_to_dict")
async def test_update_user(row_to_dict, mock_update_user, mock_session, test_user_id):
    updated_user = UserDetailUpdate(
        name="John",
        surname="Doe",
        username="johndoe",
        phone_number="1234567890",
        email="johndoe@example.com",
    )
    row_to_dict.return_value = updated_user.model_dump()
    user = AsyncMock(id=1)
    response = await UserService(mock_session).update_user(updated_user, user)
    assert response.message == "User updated successfully"
    mock_update_user.assert_called_once_with(
        user_id=user.id, data=updated_user.model_dump(exclude_none=True)
    )


@patch("src.services.auth.user_service.UserRepository.update_user")
@patch("src.services.auth.user_service.UserRepository.row_to_dict")
async def test_update_user_empty(row_to_dict, mock_update_user, mock_session, test_user_id):
    updated_user = UserDetailUpdate()
    row_to_dict.return_value = updated_user.model_dump()
    user = AsyncMock(id=1)
    response = await UserService(mock_session).update_user(updated_user, user)
    assert response.message == "User updated successfully"
    mock_update_user.assert_called_once_with(
        user_id=user.id, data=updated_user.model_dump(exclude_none=True)
    )


@patch("src.services.auth.user_service.UserRepository.update_user")
@patch("src.services.auth.user_service.UserRepository.row_to_dict")
async def test_update_user_fail(row_to_dict, mock_update_user, mock_session, test_user_id):
    updated_user = UserDetailUpdate(
        name="John",
        surname="Doe",
        username="johndoe",
        phone_number="1234567890",
        email="johndoe@example.com",
    )
    user = AsyncMock(id=1)
    with pytest.raises(Exception):
        await UserService(mock_session).update_user(updated_user, user)


@patch("src.services.auth.user_service.UserRepository.row_to_dict")
async def test_user_detail(row_to_dict, user_detail, mock_session):
    row_to_dict.return_value = user_detail
    response = await UserService(mock_session).user_detail(AsyncMock())
    assert response.message == "Success"


@patch("src.services.auth.user_service.UserRepository.row_to_dict")
async def test_user_detail_fail(row_to_dict, mock_session):
    row_to_dict.return_value = None
    with pytest.raises(Exception):
        await UserService(mock_session).user_detail(AsyncMock())
