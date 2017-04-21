from django.contrib import admin
from django.utils.text import ugettext_lazy as _

from codeschool import panels
from codeschool.questions.admin import QuestionAdmin
from . import models

admin.site.register(models.NumericQuestion)
admin.site.register(models.NumericProgress)
admin.site.register(models.NumericSubmission)
admin.site.register(models.NumericFeedback)


class NumericQuestionAdmin(QuestionAdmin):

    class Meta:
        model = models.NumericQuestion

    content_panels = QuestionAdmin.content_panels + [
        panels.MultiFieldPanel([
            panels.FieldPanel('correct_answer'),
            panels.FieldPanel('tolerance'),
            panels.FieldPanel('label'),
            panels.FieldPanel('help_text'),
        ], heading=_('Numeric value'))
    ]
    content_panels.append(content_panels.pop(-2))
