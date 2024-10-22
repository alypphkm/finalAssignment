from django.apps import AppConfig


class AbhallbookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ABhallbooking'

class ABhallbookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ABhallbooking'

    def ready(self):
        import ABhallbooking.signals


