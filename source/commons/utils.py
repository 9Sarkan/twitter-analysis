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


MOBILE_NUMBER_VALIDATOR = RegexValidator(
    regex=r"^\+[0-9]{1,15}$",
    message=_(
        "Input does not match pattern +98999999999 (following the "
        "E.164 recommendation)."
    ),
)

re_mobile = "^09[0-9][0-9]{8}$"
PHONE_NUMBER_VALIDATOR = RegexValidator(
    regex=re_mobile, flags=re.UNICODE, message=_("Mobile number is not valid.")
)

re_zip_code = "^[0-9]{5}[0-9]{5}$"
POSTAL_CODE_VALIDATOR = RegexValidator(
    regex=re_zip_code, flags=re.UNICODE, message=_("Postal code is not valid.")
)

re_national_code_number = "^[0-9]*$"
NATIONAL_ID_VALIDATOR = RegexValidator(
    regex=re_national_code_number,
    flags=re.UNICODE,
    message=_("Please use the english numbers."),
)


def get_active_lang():
    language = get_language()
    if not language:
        language = settings.LANGUAGE_CODE
    return language.split("-")[0]


def switch_lang_code(path_, language):
    lang_codes = [c for (c, name) in settings.LANGUAGES]

    if path_ == "":
        raise Exception("URL path for language switch is empty")
    elif path_[0] != "/":
        raise Exception('URL path for language switch does not start with "/"')
    elif language not in lang_codes:
        raise Exception("%s is not a supported language code" % language)

    parts = path_.split("/")
    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = "/" + language
    return "/".join(parts)
