from tests.conftest import get_token


async def test_delete_user_itself(client, valid_user):
    another_user = valid_user.model_copy()
    another_user.email += "m"
    another_user.login += "wqd"
    resp = await client.post("/users/registration/", data=valid_user.model_dump_json())
    assert resp.status_code == 201
    user_id = resp.json()["id"].__str__()
    resp = await client.post(
        "/users/registration/", data=another_user.model_dump_json()
    )
    assert resp.status_code == 201
    another_user_id = resp.json()["id"].__str__()

    # w/o token itself
    resp = await client.delete(f"/users/{user_id}/")
    assert resp.status_code == 401
    # w token itself
    user_token = get_token(user_id=user_id)
    resp = await client.delete(f"/users/{user_id}/", headers=user_token)
    assert resp.status_code == 403
    # w token another
    another_user_token = get_token(user_id=another_user_id)
    resp = await client.delete(f"/users/{another_user_id}/", headers=another_user_token)
    assert resp.status_code == 403


async def test_patch_and_delete_user_admin_roles(client, valid_user, create_admins):
    resp = await client.post("/users/registration/", data=valid_user.model_dump_json())
    assert resp.status_code == 201
    user_id = resp.json()["id"].__str__()
    admin_token = get_token(user_id=create_admins[0])
    service_token = get_token(user_id=create_admins[1])

    resp = await client.delete(f"/users/{user_id}/", headers=admin_token)
    assert resp.status_code == 200
    assert resp.json() == {"message": "User deleted", "user_id": user_id}
    resp = await client.patch(f"/admin/activate/{user_id}/", headers=admin_token)
    assert resp.status_code == 200

    resp = await client.delete(f"/users/{user_id}/", headers=service_token)
    assert resp.status_code == 200
    assert resp.json() == {"message": "User deleted", "user_id": user_id}
    resp = await client.patch(f"/admin/activate/{user_id}/", headers=service_token)
    assert resp.status_code == 200


async def test_delete_admin(client, create_admins):
    admin_token = get_token(user_id=create_admins[0])
    service_token = get_token(user_id=create_admins[1])

    resp = await client.delete(f"/users/{create_admins[0]}/", headers=admin_token)
    assert resp.status_code == 403
    resp = await client.delete(f"/users/{create_admins[1]}/", headers=admin_token)
    assert resp.status_code == 403
    resp = await client.delete(f"/users/{create_admins[0]}/", headers=service_token)
    assert resp.status_code == 200
    resp = await client.delete(f"/users/{create_admins[1]}/", headers=service_token)
    assert resp.status_code == 403
