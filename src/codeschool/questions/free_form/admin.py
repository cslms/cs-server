from django.utils.text import ugettext_lazy as _

from codeschool import panels
from codeschool.questions.admin import QuestionAdmin
from . import models


class CodeQuestionAdmin(QuestionAdmin):

    class Meta:
        model = models.FreeFormQuestion

    content_panels = [
        ...,

        panels.MultiFieldPanel([
            panels.FieldPanel('type'),
            panels.FieldPanel('filter'),
        ], heading=_('Options')),
    ]
