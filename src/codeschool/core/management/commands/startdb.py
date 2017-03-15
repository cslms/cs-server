import importlib

from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'loads required initial data for codeschool.'

    def add_arguments(self, parser):
        parser.add_argument('--recommended', '-r', action='store_true')
        parser.add_argument('--demo', '-d', action='store_true')

    def handle(self, *args, demo=False, recommended=False, **options):
        # Choose list of methods
        methods = []
        if demo:
            methods.append('demo')
        if recommended:
            methods.append('recommended')

        # Load data using each method
        for app in apps.app_configs.values():
            mod_path = app.module.__name__
            try:
                importlib.import_module(mod_path + '.fixtures')
            except ImportError:
                continue

            for method in methods:
                path = mod_path + '.fixtures.' + method
                try:
                    mod = importlib.import_module(path)
                    loader = mod.load
                except (ImportError, AttributeError):
                    continue
                else:
                    loader()
                    print('Loaded data from %s (%s).' % (mod_path, method))
