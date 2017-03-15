from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.questions.models import Question, QuestionProgress, \
    QuestionSubmission, QuestionFeedback

# Text formats
formats = [
    'markdown:Markdown',
    'text:Plain Text',
    'html:HTML',
    'css:CSS',
    'latex:LaTeX',
    'tex:TeX',
    'ruby:Ruby',
    'java:Java',
    'javascript:Javascript',
    'perl:Perl',
    'haskell:Haskell',
    'julia:Julia',
    'go:Go',
    'pytuga:Pytuguês',
    'python:Python 3.5',
    'python2:Python 2.7',
    'c:C99 (gcc compiler)',
    'cpp:C++11',
]


class FreeTextQuestion(Question):
    TYPE_CODE = 0
    TYPE_RICHTEXT = 1

    text_type = models.IntegerField(
        _('Text type'),
        choices=[
            (TYPE_CODE, _('Code')),
            (TYPE_RICHTEXT, _('Rich text')),
        ],
        default=TYPE_CODE,
    )
    syntax_highlight = models.CharField(
        choices=[x.split(':') for x in formats],
        default='python',
        help_text=_(
            'Syntax highlight for code based questions.'
        ),
    )


class FreeTextProgress(QuestionProgress):
    pass


class FreeTextSubmission(QuestionSubmission):
    text = models.TextField()


class FreeTextFeedback(QuestionFeedback):
    pass
