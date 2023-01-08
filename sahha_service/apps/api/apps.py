from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ApiConfig(AppConfig):
    label = 'api'
    name = 'sahha_service.apps.api'
    verbose_name = _('API')
