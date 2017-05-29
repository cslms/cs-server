from enum import IntEnum

from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.questions.models import Question, QuestionProgress, \
    QuestionSubmission, QuestionFeedback


class Type(IntEnum):
    PHYSICAL = 0
    CODE = 1
    RICHTEXT = 2
    FILE = 3


class FreeFormQuestion(Question):
    """
    A free form question is *not* automatically graded.

    The student can submit a resource that can be a text, code, file, image,
    etc and a human has to analyse and grade it manually.
    """

    Type = Type
    type = models.IntegerField(
        _('Text type'),
        choices=[
            (Type.CODE.value, _('Code')),
            (Type.RICHTEXT.value, _('Rich text')),
            (Type.FILE.value, _('File')),
            (Type.PHYSICAL.value, _('Physical delivery')),
        ],
        default=Type.CODE,
    )
    filter = models.CharField(
        _('filter'),
        max_length=30,
        blank=True,
        help_text=_(
            'Filters the response by some criteria.'
        ),
    )

    class Meta:
        autograde = False


class FreeFormProgress(QuestionProgress):
    """
    Progress object for free form questions.
    """


class FreeFormSubmission(QuestionSubmission):
    """
    Submission object for free form questions.
    """

    data = models.TextField(blank=True)
    metadata = models.CharField(blank=True, max_length=200)


class FreeFormFeedback(QuestionFeedback):
    """
    Feedback object for free form questions.
    """
