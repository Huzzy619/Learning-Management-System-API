from django.apps import AppConfig


class LearnConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "learn"


    def ready(self) -> None:
        # import learn.signals.handlers 
        pass