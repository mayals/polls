from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
       
    # Note: signal NOT work without this code in case that signals outside models.py:
    def ready(self):
        import users.signals
