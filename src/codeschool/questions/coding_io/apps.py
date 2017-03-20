from django.apps import AppConfig


class CodingIoConfig(AppConfig):
    name = 'coding_io'

    def ready(self):
        # Register files
        from . import render
