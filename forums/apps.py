from django.apps import AppConfig


# class ForumsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'forums'

class YourAppConfig(AppConfig):
    name = 'forums'

    def ready(self):
        import forums.signals