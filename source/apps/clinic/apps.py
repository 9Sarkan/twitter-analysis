from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SampleAppConfig(AppConfig):
    name = 'apps.SampleApp'
    verbose_name = _('SampleApps')
