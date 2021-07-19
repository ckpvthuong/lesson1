from django.apps import AppConfig


class SurveyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module.survey'
    verbose_name = 'Khảo sát'
    label = 'survey'

    def ready(self):
        import module.survey.signals
