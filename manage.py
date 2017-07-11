import sys

import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codeschool.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
