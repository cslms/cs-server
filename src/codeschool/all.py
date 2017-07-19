"""
Import most models and useful function into the same namespace. Should be used
only in the cli.
"""
# flake8: noqa

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'codeschool.settings.local'
import django
django.setup()
from django.apps import apps
from annoying.functions import get_config

from .types.deferred import Deferred
from .settings import dev as settings
from django.contrib.auth.models import *


# Core modules
from .core.files.models import *
from .core.services.models import *
from .core.users.models import *
from .core.config.models import *

python = Deferred(ProgrammingLanguage.objects.get, ref='python')
user = Deferred(lambda: User.objects.first())


# LMS models
from .lms.activities.models import *
from .lms.activity_lists.models import *
from .lms.attendance.models import *
# from .lms.calendars.models import *
from .lms.classrooms.models import *
from .lms.organizations.models import *


# Extra
# from .extra.code_carrousel.models import *
# from .extra.code_exhibit.models import *


# Gamification
#from .gamification.badges.models import *
#from .gamification.points.models import *


# Methods
#from .methods.kanban.models import *
#from .methods.pairings_boards.models import *
#from .methods.sentiment_boards.models import *
#from .methods.sprints.models import *


# Questions
from .questions.base.models import *
from .questions.code.models import *
from .questions.coding_io.models import *
# from .questions.form.models import *
from .questions.free_form.models import *
#from .questions.multiple_choice.models import *
from .questions.numeric.models import *
from .questions.text.models import *


# Social
#from .social.feed.models import *
from .social.friends.models import *
#from .social.teams.models import *
