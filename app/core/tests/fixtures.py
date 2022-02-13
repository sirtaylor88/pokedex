import pytest

from rest_framework.test import APIClient


@pytest.fixture
def user_log(user_factory):
    """Return an user"""

    return user_factory(username="tai")


@pytest.fixture
def client_log(user_log):
    """Create an user and login"""

    client_log = APIClient()
    client_log.force_authenticate(user_log)

    return client_log
