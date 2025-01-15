from tests.conftest import get_token


async def test_get_me_auth(client, valid_user):
    resp = await client.post("/users/registration/", data=valid_user.model_dump_json())
    assert resp.status_code == 201
    post_data = resp.json()
    token_header = get_token(post_data["id"])
    resp = await client.get("/users/me/", headers=token_header)
    assert resp.status_code == 200
    get_data = resp.json()
    assert get_data == {
        "id": post_data["id"],
        "login": post_data["login"],
        "email": post_data["email"],
        "name": None,
        "lastname": None,
    }


async def test_get_me_unauth(client, valid_user):
    resp = await client.post("/users/registration/", data=valid_user.model_dump_json())
    assert resp.status_code == 201
    post_data = resp.json()
    token_header = get_token(post_data["id"] + "123")
    resp = await client.get("/users/me/", headers=token_header)
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Could not validate credentials"}


async def test_get_user():
    pass
