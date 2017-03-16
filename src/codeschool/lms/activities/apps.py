from django.apps import AppConfig

class ActivitiesConfig(AppConfig):
    name = 'codeschool.lms.activities'

    def ready(self):
        from codeschool.lms.activities import models

        for base in ['Activity', 'Submission']:
            model = getattr(models, base)
            for cls in model._subclasses:
                if not cls._meta.abstract:
                    cls._register_subclass()
