import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_env(key: str, default=None, raise_exception=False):
    value = os.environ.get(key, default=default)
    if raise_exception:
        if not value:
            raise ImproperlyConfigured(f"You most set {key} variable in env")
    return value

