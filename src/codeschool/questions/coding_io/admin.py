from django.contrib import admin
from django.utils.text import ugettext_lazy as _

from codeschool import panels
from codeschool.questions.admin import QuestionAdmin
from . import models

admin.site.register(models.AnswerKey)
admin.site.register(models.CodingIoFeedback)
admin.site.register(models.CodingIoProgress)
admin.site.register(models.CodingIoSubmission)
admin.site.register(models.CodingIoQuestion)
admin.site.register(models.TestState)


class CodingIoQuestionAdmin(QuestionAdmin):

    class Meta:
        model = models.CodingIoQuestion

    content_panels = QuestionAdmin.content_panels[:]
    content_panels.insert(-1, panels.MultiFieldPanel([
        panels.FieldPanel('num_pre_tests'),
        panels.FieldPanel('pre_tests_source'),
    ], heading=_('Pre-tests definitions')))
    content_panels.insert(-1, panels.MultiFieldPanel([
        panels.FieldPanel('num_post_tests'),
        panels.FieldPanel('post_tests_source'),
    ], heading=_('Post-tests definitions')))
    content_panels.insert(
        -1,
        panels.InlinePanel('answers', label=_('Answer keys'))
    )

    settings_panels = QuestionAdmin.settings_panels + [
        panels.MultiFieldPanel([
            panels.FieldPanel('language'),
            panels.FieldPanel('timeout'),
        ], heading=_('Options'))
    ]
