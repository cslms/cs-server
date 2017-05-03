from django.utils.translation import ugettext_lazy as _
from iospec.feedback import Feedback
from lazyutils import lazy, delegate_to

from codeschool import models
from codeschool.questions.coding_io.ejudge import grade_code
from codeschool.questions.models import QuestionFeedback
from ..render import render


class CodingIoFeedback(QuestionFeedback):
    for_pre_test = models.BooleanField(
        _('Grading pre-test?'),
        default=False,
        help_text=_(
            'True if its grading in the pre-test phase.'
        )
    )
    json_feedback = models.JSONField(blank=True, null=True)
    feedback_status = property(lambda x: x.feedback.status)
    is_wrong_answer = delegate_to('feedback')
    is_presentation_error = delegate_to('feedback')
    is_timeout_error = delegate_to('feedback')
    is_build_error = delegate_to('feedback')
    is_runtime_error = delegate_to('feedback')

    @lazy
    def feedback(self):
        if self.json_feedback:
            return Feedback.from_json(self.json_feedback)
        else:
            return None

    def get_tests(self):
        """
        Return an iospec object with the tests for the current correction.
        """

        if self.for_pre_test:
            return self.question.get_expanded_pre_tests()
        else:
            return self.question.get_expand_post_tests()

    def get_autograde_value(self):
        tests = self.get_tests()
        source = self.submission.source
        language_ref = self.submission.language.ejudge_ref()
        feedback = grade_code(source, tests,
                              lang=language_ref,
                              timeout=self.question.timeout)

        return feedback.grade * 100, {'json_feedback': feedback.to_json()}

    def render_message(self, **kwargs):
        return render(self.feedback)
