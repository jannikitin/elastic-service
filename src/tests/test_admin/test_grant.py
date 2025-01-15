from tests.conftest import get_token


async def test_grant_and_remove(client, create_admins):

    admin_token = get_token(user_id=create_admins[0])
    service_token = get_token(user_id=create_admins[1])

    resp = await client.patch(
        f"/admin/service/grant/{create_admins[0]}/", headers=admin_token
    )
    assert resp.status_code == 409
    assert resp.json() == {"detail": "User is already granted"}

    resp = await client.patch(
        f"/admin/service/remove/{create_admins[0]}/", headers=service_token
    )
    assert resp.status_code == 200

    resp = await client.patch(
        f"/admin/service/grant/{create_admins[0]}/", headers=admin_token
    )
    assert resp.status_code == 403
    assert resp.json() == {"detail": "Forbidden"}

    resp = await client.patch(
        f"/admin/service/grant/{create_admins[0]}/", headers=service_token
    )
    assert resp.status_code == 200
