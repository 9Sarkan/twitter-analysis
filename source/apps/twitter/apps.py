from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TwitterAppConfig(AppConfig):
    name = 'apps.TwitterApp'
    verbose_name = _('TwitterApp')
