from django.apps import AppConfig

class HarpstroyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'harpstroy'
    
    def ready(self):
        import harpstroy.signals  # noqa