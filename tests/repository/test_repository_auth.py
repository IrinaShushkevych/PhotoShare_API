import pytest
from fastapi import HTTPException

from src.schemas import UserModel, Role, UserUpdateModel
import src.repositories.auth as rep_auth
from src.config.settings import messages


@pytest.mark.asyncio
async def test_create_user(user, session):
    new_user = UserModel(email=user['email'], username=user['username'], password=user['password'], role=Role.admin)
    response = await rep_auth.create_user(body=new_user, db=session)
    assert response.email == user['email']
    assert response.username == user['username']
    assert response.password == user['password']
    assert response.role == Role.admin


@pytest.mark.asyncio
async def test_recreate_user(user, session):
    new_user = UserModel(email=user['email'], username=user['username'], password=user['password'], role=Role.admin)
    with pytest.raises(HTTPException) as exception:
        await rep_auth.create_user(body=new_user, db=session)
    assert messages.user_exists in str(exception)


@pytest.mark.asyncio
async def test_get_user_by_email(user, session):
    response = await rep_auth.get_user_by_email(user['email'], session)
    assert response.email == user['email']
    assert response.username == user['username']
    assert response.password == user['password']
    assert response.role == Role.admin


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(wrong_user, session):
    response = await rep_auth.get_user_by_email(wrong_user['email'], session)
    assert response is None


@pytest.mark.asyncio
async def test_update_user(user, session):
    new_data = UserUpdateModel(firstname='Test', lastname='Testing')
    response = await rep_auth.update_user(user['email'], new_data, session)
    assert response.username == user['username']
    assert response.firstname == new_data.firstname
    assert response.lastname == new_data.lastname
    assert response.password == user['password']


@pytest.mark.asyncio
async def test_update_user_not_found(wrong_user, session):
    new_data = UserUpdateModel(firstname='Test', lastname='Testing')
    response = await rep_auth.update_user(wrong_user['email'], new_data, session)
    assert response is None


@pytest.mark.asyncio
async def test_update_avatar(user, session):
    avatar_url = 'http://hello.com'
    response = await rep_auth.update_avatar(user['email'], avatar_url, session)
    assert response.username == user['username']
    assert response.avatar == avatar_url


@pytest.mark.asyncio
async def test_update_password(user, session):
    password = 'asdfg-456'
    response = await rep_auth.update_password(user['email'], password, session)
    assert response.username == user['username']
    assert response.password == password


@pytest.mark.asyncio
async def test_change_active(user, session):
    response = await rep_auth.change_active(user['email'], False, session)
    assert response.username == user['username']
    assert response.is_active is False
