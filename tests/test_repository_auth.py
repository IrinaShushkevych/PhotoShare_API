import unittest
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
import src.repositories.auth as rep_auth
from src.config.settings import messages


@pytest.mark.asyncio
async def test_create_user(user, session):
    response = await rep_auth.create_user(user, session)
    assert response.email == user.email
    assert response.username == user.username
    assert response.password == user.password
