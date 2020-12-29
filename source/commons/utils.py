import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import RegexValidator


def get_env(key: str, default=None, raise_exception=False):
    value = os.environ.get(key, default=default)
    if raise_exception:
        if not value:
            raise ImproperlyConfigured(f"You most set {key} variable in env")
    return value


PHONE_NUMBER_VALIDATOR = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message=
    "Phone number must be entered in the format:"
    "'+999999999'. Up to 15 digits allowed."
)
