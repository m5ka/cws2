import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

validate_username_regex = RegexValidator(
    re.compile(r"^[a-zA-Z0-9-_.]+\Z"),
    _("Username may only contain letters, numbers, hyphens, underscores and dots."),
    "invalid",
)


validate_colour_code_regex = RegexValidator(
    re.compile(r"^#[A-Fa-f0-9]{6}\Z"),
    _("Colour is not a valid hexadecimal colour code."),
    "invalid",
)


def validate_username_length(value):
    if (
        len(value) < settings.USERNAME_MIN_LENGTH
        or len(value) > settings.USERNAME_MAX_LENGTH
    ):
        raise ValidationError(
            _("Username must be between %(min_length) and %(max_length) characters.")
            % {
                "min_length": settings.USERNAME_MIN_LENGTH,
                "max_length": settings.USERNAME_MAX_LENGTH,
            }
        )
