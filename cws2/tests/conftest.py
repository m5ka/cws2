import re

import pytest

from cws2.models.user import User


@pytest.fixture(scope="session")
def re_uuid() -> re.Pattern:
    return re.compile(r"^[2-9A-HJ-NP-Za-km-z]{22}$")


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        "joe.bloggs", email="joe@conworkshop.com", password="bl0ggs123"
    )
