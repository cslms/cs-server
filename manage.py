import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


if __name__ == "__main__":
    if '--grader' in sys.argv:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs_grader.settings")
        sys.argv.remove('--grader')
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codeschool.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
