import re

import pytest
from django.utils import timezone

from cws2.models.user import User


@pytest.mark.django_db
def test_user(user: User, re_uuid: re.Pattern):
    assert isinstance(user.pk, int)
    assert user.pk > 0
    assert re_uuid.match(user.uuid) is not None
    assert not user.is_bot
    assert str(user) == "joe.bloggs"
    assert user.get_absolute_url() == "/@joe.bloggs"


@pytest.mark.django_db
def test_user_email_confirmed(user: User):
    assert user.email_confirmed_at is None
    assert not user.email_confirmed
    user.email_confirmed_at = timezone.now()
    user.save()
    assert user.email_confirmed_at is not None
    assert user.email_confirmed
