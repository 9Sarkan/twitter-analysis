import os
import re
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


def get_env_with_default(name, default):
    return os.getenv(name, default)


def get_env(name, default=None, raise_exception=False):
    value = get_env_with_default(name, default)
    if raise_exception:
        if not value:
            raise ImproperlyConfigured(f"You most set {name} variable in env")
    return value
