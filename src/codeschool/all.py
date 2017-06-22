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
user = Deferred(lambda: User.objects.first())

# Optional components -- LMS
if 'codeschool.lms.courses' in settings.INSTALLED_APPS:
    from .lms.courses.models import *
if 'codeschool.lms.attendance' in settings.INSTALLED_APPS:
    from .lms.attendance.models import *

# Optional questions
if 'codeschool.questions.coding_io' in settings.INSTALLED_APPS:
    from .questions.coding_io.models import *
    coding_io = Deferred(CodingIoQuestion.objects.first)
if 'codeschool.questions.code' in settings.INSTALLED_APPS:
    from .questions.code.models import *
    code = Deferred(CodeQuestion.objects.first)
if 'codeschool.questions.free_text' in settings.INSTALLED_APPS:
    from .questions.free_form.models import *
    free_text = Deferred(FreeFormQuestion.objects.first)
if 'codeschool.questions.numeric' in settings.INSTALLED_APPS:
    from .questions.numeric.models import *
    numeric = Deferred(NumericQuestion.objects.first)
