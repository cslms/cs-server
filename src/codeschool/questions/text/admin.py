from django.contrib import admin
from django.utils.text import ugettext_lazy as _

from codeschool import panels
from codeschool.questions.admin import QuestionAdmin
from . import models

admin.site.register(models.TextQuestion)
admin.site.register(models.TextProgress)
admin.site.register(models.TextSubmission)
admin.site.register(models.TextFeedback)


class TextQuestionAdmin(QuestionAdmin):

    class Meta:
        model = models.TextQuestion

    content_panels = QuestionAdmin.content_panels + [
        panels.MultiFieldPanel([
            panels.FieldPanel('correct_answer'),
            panels.FieldPanel('label'),
            panels.FieldPanel('help_text'),
        ], heading=_('Text value'))
    ]
    content_panels.append(content_panels.pop(-2))
