import pytest
from api.schemas.update import UserUpdateSchema
from tests.conftest import get_token


@pytest.mark.parametrize(
    "update_schema, sc, response",
    [
        (
            UserUpdateSchema(
                name="name",
                lastname="lastname",
                email="email@example.com",
                login="login",
            ),
            200,
            {
                "id": None,
                "name": "name",
                "lastname": "lastname",
                "email": "email@example.com",
                "login": "login",
            },
        ),
        (
            UserUpdateSchema(lastname="lastname", email="email@example.com"),
            200,
            {
                "id": None,
                "name": None,
                "lastname": "lastname",
                "email": "email@example.com",
                "login": "test_login",
            },
        ),
        (
            UserUpdateSchema(),
            200,
            {
                "id": None,
                "name": None,
                "lastname": None,
                "email": "test@example.com",
                "login": "test_login",
            },
        ),
    ],
)
async def test_update_user_valid(client, valid_user, update_schema, sc, response):
    resp = await client.post("/users/registration/", data=valid_user.model_dump_json())
    assert resp.status_code == 201
    user_id = resp.json()["id"]
    token = get_token(user_id)
    resp = await client.patch(
        f"/users/{user_id}/", data=update_schema.model_dump_json(), headers=token
    )
    assert resp.status_code == sc
    assert resp.json() == response


@pytest.mark.parametrize(
    "update_schema, sc",
    [
        ({"name": "a"}, 422),
        (
            {"name": "123ыфв"},
            422,
        ),
        (
            {"login": "as"},
            422,
        ),
        (
            {"email": "email"},
            422,
        ),
    ],
)
async def test_update_user_unvalid(client, valid_user, update_schema, sc):
    resp = await client.post("/users/registration/", data=valid_user.model_dump_json())
    assert resp.status_code == 201
    user_id = resp.json()["id"]
    token = get_token(user_id)
    resp = await client.patch(f"/users/{user_id}/", data=update_schema, headers=token)
    assert resp.status_code == sc
