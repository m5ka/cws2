import re

from django.utils import timezone

from cws2.models.user import User


def test_user(user: User, re_uuid: re.Pattern):
    assert user.pk == user.uuid
    assert re_uuid.match(user.pk) is not None
    assert not user.is_bot
    assert str(user) == "joe.bloggs"
    assert user.get_absolute_url() == "/@joe.bloggs"


def test_user_email_confirmed(user: User):
    assert user.email_confirmed_at is None
    assert not user.email_confirmed
    user.email_confirmed_at = timezone.now()
    user.save()
    assert user.email_confirmed_at is not None
    assert user.email_confirmed
