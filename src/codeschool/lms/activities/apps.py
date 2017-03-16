from django.apps import AppConfig


class ActivitiesConfig(AppConfig):
    name = 'codeschool.lms.activities'

    def ready(self):
        for base in ['Submission']:
            model = self.get_model(base)
            for cls in model._subclasses:
                if not cls._meta.abstract:
                    cls._register_subclass()

