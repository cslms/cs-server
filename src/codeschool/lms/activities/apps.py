from django.apps import AppConfig


class ActivitiesConfig(AppConfig):
    name = 'codeschool.lms.activities'

    def ready(self):
        model = self.get_model('Submission')

        for cls in model._subclasses:
            if not cls._meta.abstract:
                cls._register_subclass()

