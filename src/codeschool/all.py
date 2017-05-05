"""
Import most models and useful function into the same namespace. Should be used
only in the cli.
"""
# flake8: noqa

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'codeschool.settings'
import django
django.setup()


from .types.deferred import Deferred


# Unconditional imports
from . import *
from .core import *
from .core.models import *
from .lms.activities.models import *
from .questions.models import *
from . import settings
from .factories import *
from django.contrib.auth.models import *

# Example deferred objects
python = Deferred(ProgrammingLanguage.objects.get, ref='python')
user = Deferred(lambda: User.objects.all()[1])

# Optional components -- LMS
if 'codeschool.lms.courses' in settings.INSTALLED_APPS:
    from .lms.courses.models import *
if 'codeschool.lms.attendance' in settings.INSTALLED_APPS:
    from .lms.attendance.models import *

# Optional questions
if 'codeschool.questions.coding_io' in settings.INSTALLED_APPS:
    from .questions.coding_io.models import *
    coding_io = Deferred(CodingIoQuestion.objects.first)
if 'codeschool.questions.coding_func' in settings.INSTALLED_APPS:
    from .questions.coding_func.models import *
    coding_func = Deferred(CodingFuncQuestion.objects.first)
if 'codeschool.questions.free_text' in settings.INSTALLED_APPS:
    from .questions.free_text.models import *
    free_text = Deferred(FreeTextQuestion.objects.first)
if 'codeschool.questions.numeric' in settings.INSTALLED_APPS:
    from .questions.numeric.models import *
    numeric = Deferred(NumericQuestion.objects.first)
if 'codeschool.sparta' in settings.INSTALLED_APPS:
    from .sparta.models import *
    sparta = Deferred(SpartaActivity.objects.first)
    sparta_group = Deferred(lambda: sparta.groups.first())
