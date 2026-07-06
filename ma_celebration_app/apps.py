from django.apps import AppConfig


class MaCelebrationAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ma_celebration_app'

    def ready(self):
        from . import signals
