import srvice
from django.utils.translation import ugettext_lazy as _

import codeschool.mixins
from codeschool import blocks
from codeschool import models
from codeschool.lms.activities.models import Activity, Submission, Progress
from codeschool.lms.activities.models.feedback import Feedback

QUESTION_BODY_BLOCKS = [
    ('paragraph', blocks.RichTextBlock()),
    ('heading', blocks.CharBlock(classname='full title')),
    ('markdown', blocks.MarkdownBlock()),
    ('html', blocks.RawHTMLBlock()),
]


class Question(models.DecoupledAdminPage,
               codeschool.mixins.ShortDescriptionPageMixin,
               Activity):
    """
    Base abstract class for all question types.
    """

    class Meta:
        abstract = True
        permissions = (("download_question", "Can download question files"),)

    body = models.StreamField(
        QUESTION_BODY_BLOCKS,
        blank=True,
        null=True,
        verbose_name=_('Question description'),
        help_text=_(
            'Describe what the question is asking and how should the students '
            'answer it as clearly as possible. Good questions should not be '
            'ambiguous.'
        ),
    )
    comments = models.RichTextField(
        _('Comments'),
        blank=True,
        help_text=_('(Optional) Any private information that you want to '
                    'associate to the question page.')
    )
    import_file = models.FileField(
        _('import question'),
        null=True,
        blank=True,
        upload_to='question-imports',
        help_text=_(
            'Fill missing fields from question file. You can safely leave this '
            'blank and manually insert all question fields.'
        )
    )
    _subclass_root = 'Question'
    instant_autograde = True

    # Serve pages
    def get_submission_kwargs(self, request, kwargs):
        return {}

    def get_context(self, request, *args, **kwargs):
        context = dict(
            super().get_context(request, *args, **kwargs),
            question=self,
            form_name='response-form',
        )
        return context

    #
    # Routes
    #
    def serve_ajax_submission(self, client, **kwargs):
        """
        Serve AJAX request for a question submission.
        """
        kwargs = self.get_submission_kwargs(client.request, kwargs)
        submission = self.submit(client.request, **kwargs)
        if submission.recycled:
            client.dialog(html='You already submitted this response!')
        elif self.instant_autograde:
            feedback = submission.auto_feedback()
            data = feedback.render_message()
            client.dialog(html=data)
        else:
            client.dialog(html='Your submission is on the correction queue!')

    @srvice.route(r'^submit-response.api/$', name='submit-ajax')
    def route_ajax_submission(self, client, **kwargs):
        return self.serve_ajax_submission(client, **kwargs)


class QuestionMixin:
    """
    Shared properties for submissions, progress and feedback models.
    """
    question = property(lambda x: x.activity)
    question_id = property(lambda x: x.activity_id)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        if question is not None:
            kwargs.setdefault('activity', question)
        super().__init__(*args, **kwargs)


class QuestionSubmission(QuestionMixin, Submission):
    """
    Abstract class for submissions to questions.
    """

    class Meta:
        abstract = True


class QuestionProgress(QuestionMixin, Progress):
    """
    Abstract class for keeping up with the progress of student responses.
    """

    class Meta:
        abstract = True


class QuestionFeedback(QuestionMixin, Feedback):
    """
    Abstract class for representing feedback to users.
    """

    class Meta:
        abstract = True
