import json

import pytest
from httpx import AsyncClient

ENDPOINT = "/api/v1/user"


async def test_delete_user_me(ac: AsyncClient, get_token):
    response = await ac.delete(f"{ENDPOINT}/me", headers={"Authorization": f"Bearer {get_token}"})
    assert response.status_code == 200
    assert "User deleted successfully" in response.text


async def test_delete_user_me_fail(ac: AsyncClient, exp_token):
    response = await ac.delete(f"{ENDPOINT}/me", headers={"Authorization": f"Bearer {exp_token}"})
    assert response.status_code == 401
    assert "Wrong credentials" in response.text


@pytest.mark.parametrize("get_token", [{"role": "admin"}, {"role": "moderator"}], indirect=True)
async def test_get_filtered_users(ac: AsyncClient, get_token, create_user):
    user = await create_user()
    response = await ac.get(
        f"{ENDPOINT}/?page=1&limit=5&filter_by_name={user.name}&sort_by=name&order_by=desc",
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 200
    assert "users" in response.json()["payload"]
    assert response.json()["message"] == "Success"


@pytest.mark.parametrize("get_token", [{"role": "user"}], indirect=True)
async def test_get_filtered_users_fail(ac: AsyncClient, get_token, create_user):
    await create_user()
    response = await ac.get(
        f"{ENDPOINT}/?page=1&limit=5", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 403
    assert "Not enough permissions" in response.text


@pytest.mark.parametrize("get_token", [{"role": "admin"}, {"role": "moderator"}], indirect=True)
async def test_get_user_by_id(ac: AsyncClient, create_user, get_token):
    user = await create_user()
    response = await ac.get(
        f"{ENDPOINT}/user/{user.id}", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    assert response.json()["payload"]["name"] == user.name
    assert response.json()["message"] == "Success"


@pytest.mark.parametrize("get_token", [{"role": "user"}], indirect=True)
async def test_get_user_by_id_fail(ac: AsyncClient, create_user, get_token):
    user = await create_user()
    response = await ac.get(
        f"{ENDPOINT}/user/{user.id}", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 403
    assert "Not enough permissions" in response.text


async def test_get_user_by_id_me(ac: AsyncClient, get_token):
    response = await ac.get(f"{ENDPOINT}/me", headers={"Authorization": f"Bearer {get_token}"})
    assert response.status_code == 200
    assert len(response.json()["payload"]) > 1
    assert response.json()["message"] == "Success"


async def test_get_user_by_id_me_fail(ac: AsyncClient, get_token, exp_token):
    response = await ac.get(f"{ENDPOINT}/me", headers={"Authorization": f"Bearer {exp_token}"})
    assert response.status_code == 401
    assert "Wrong credentials" in response.text


@pytest.mark.parametrize("get_token", [{"role": "admin"}], indirect=True)
async def test_patch_user_by_id(ac: AsyncClient, create_user, get_token):
    user = await create_user()
    data_dict = {"name": "kate"}
    response = await ac.patch(
        f"{ENDPOINT}/user/{user.id}",
        headers={"Authorization": f"Bearer {get_token}"},
        data=json.dumps(data_dict),
    )
    assert response.status_code == 200
    assert response.json()["payload"]["name"] == "kate"
    assert "User updated successfully" in response.text


@pytest.mark.parametrize("get_token", [{"role": "user"}, {"role": "moderator"}], indirect=True)
async def test_patch_user_by_id_fail(ac: AsyncClient, create_user, get_token):
    user = await create_user()
    data_dict = {"name": "kate"}
    response = await ac.patch(
        f"{ENDPOINT}/user/{user.id}",
        headers={"Authorization": f"Bearer {get_token}"},
        data=json.dumps(data_dict),
    )
    assert response.status_code == 403
    assert "Not enough permissions" in response.text


async def test_patch_user_me(ac: AsyncClient, get_token):
    data_dict = {"name": "MOON"}
    response = await ac.patch(
        f"{ENDPOINT}/me",
        headers={"Authorization": f"Bearer {get_token}"},
        data=json.dumps(data_dict),
    )
    assert response.status_code == 200
    assert response.json()["payload"]["name"] == "MOON"
    assert "User updated successfully" in response.text


async def test_patch_user_me_fail(ac: AsyncClient, exp_token):
    data_dict = {"name": "MOON"}
    response = await ac.patch(
        f"{ENDPOINT}/me",
        headers={"Authorization": f"Bearer {exp_token}"},
        data=json.dumps(data_dict),
    )
    assert response.status_code == 401
    assert "Wrong credentials" in response.text
