from django.apps import AppConfig


class CliConfig(AppConfig):
    name = 'codeschool.cli'

    def ready(self):
        from . import methods  # noqa: F401
