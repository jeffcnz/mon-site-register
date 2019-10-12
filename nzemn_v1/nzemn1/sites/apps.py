from django.apps import AppConfig
import sites.signals.handlers 

class SitesConfig(AppConfig):
    name = 'sites'


class AgencysConfig(AppConfig):
    name = 'agencys'

    def ready(self):
        import sites.signals.handlers
