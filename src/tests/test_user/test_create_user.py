import json

import pytest


async def test_create_user(client, valid_user):
    resp = await client.post("/users/registration/", data=valid_user.model_dump_json())
    user_data = resp.json()
    assert resp.status_code == 201
    assert user_data["email"] == valid_user.email
    assert user_data["login"] == valid_user.login


async def test_create_user_already_exists(client, valid_user):
    unvalid_login = valid_user.model_copy()
    unvalid_login.email += "mmm"

    unvalid_email = valid_user.model_copy()
    unvalid_email.login += "1"

    resp_first = await client.post(
        "/users/registration/", data=valid_user.model_dump_json()
    )
    resp_unvfull = await client.post(
        "/users/registration/", data=valid_user.model_dump_json()
    )
    resp_unvlogin = await client.post(
        "/users/registration/", data=unvalid_login.model_dump_json()
    )
    resp_unvemail = await client.post(
        "/users/registration/", data=unvalid_email.model_dump_json()
    )

    assert resp_first.status_code == 201
    assert resp_unvfull.status_code == 409
    assert resp_unvlogin.status_code == 409
    assert resp_unvemail.status_code == 409

    assert resp_unvfull.json() == resp_unvlogin.json() == resp_unvemail.json()


@pytest.mark.parametrize(
    "user, status_code",
    [
        ({"email": "", "login": "", "password": ""}, 422),
        ({"email": "valid_email@example.com", "login": "", "password": ""}, 422),
        (
            {
                "email": "valid_email@example.com",
                "login": "valid_login",
                "password": "",
            },
            422,
        ),
        (
            {
                "email": "valid_email@example.com",
                "login": "valid_login",
                "password": "123Adq",
            },
            422,
        ),
    ],
)
async def test_create_unvalid_user(client, user, status_code):
    resp = await client.post("/users/registration/", data=json.dumps(user))
    assert resp.status_code == status_code
