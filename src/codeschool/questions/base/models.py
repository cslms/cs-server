from django.utils.translation import ugettext_lazy as _

import bricks.rpc
from bricks.html5 import p, div, h2
from codeschool import blocks
from codeschool import mixins
from codeschool import models
from codeschool.lms.activities.models import Activity, Submission, Progress
from codeschool.lms.activities.models.feedback import Feedback

QUESTION_BODY_BLOCKS = [
    ('paragraph', blocks.RichTextBlock()),
    ('heading', blocks.CharBlock(classname='full title')),
    ('markdown', blocks.MarkdownBlock()),
    ('html', blocks.RawHTMLBlock()),
]


class Question(mixins.ShortDescriptionPage, Activity):
    """
    Base abstract class for all question types.
    """

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

    class Meta:
        abstract = True
        permissions = (("download_question", "Can download question files"),)

    def get_navbar(self, user):
        """
        Returns the navbar for the given question.
        """

        from .bricks import navbar_question

        return navbar_question(self, user)

    #
    # Ajax submissions for user responses
    #
    def render_from_submission(self, submission):
        """
        Render a user-facing message from the supplied submission.
        """

        if not self._meta.autograde:
            return \
                div()[
                    h2('Congratulations!'),
                    p(_('Submission sent! Please wait while someone will '
                        'grade it!')),
                ]

        # Check options for autograde questions
        if submission.recycled and submission.has_feedback:
            feedback = submission.feedback
            return feedback.render_message()
        elif self._meta.instant_feedback:
            feedback = submission.auto_feedback()
            return feedback.render_message()
        else:
            return _('Your submission is on the correction queue!')

    def serve_ajax_submission(self, client, **kwargs):
        """
        Serve AJAX request for a question submission.
        """

        submission = self.submit_with_user_payload(client.request, kwargs)
        data = self.render_from_submission(submission)
        client.dialog(html=data)

    @bricks.rpc.route(r'^submit-response.api/$', name='submit-ajax')
    def route_ajax_submission(self, client, **kwargs):
        return self.serve_ajax_submission(client, **kwargs)


class QuestionMixin:
    """
    Shared properties for submissions, progress and feedback models.
    """

    question = property(lambda x: x.activity)
    question_id = property(lambda x: x.activity_id)


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


# Update the Question._meta attribute
Question._meta.submission_class = QuestionSubmission
Question._meta.progress_class = QuestionProgress
Question._meta.feedback_class = QuestionFeedback
