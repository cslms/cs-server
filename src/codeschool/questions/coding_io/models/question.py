import logging

from annoying.functions import get_config
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

import bricks.rpc
from codeschool import models
from codeschool.core import get_programming_language
from codeschool.core.models import ProgrammingLanguage
from codeschool.fixes.parent_refresh import register_parent_prefetch
from codeschool.questions.coding_io.models import TestState
from codeschool.questions.models import Question
from iospec import parse as parse_iospec, IoSpec
from .submission import CodingIoSubmission
from .. import ejudge
from .. import validators
from lazyutils import lazy, delegate_to
from .data_access import DataAccess
from .validation import Validation

logger = logging.getLogger('codeschool.questions.coding_io')


class Placeholder(models.Model):

    placeholder = models.TextField(
        _('placeholder source code'),
        blank=True,
        help_text=_(
            'This optional field controls which code should be placed in '
            'the source code editor when a question is opened. This is '
            'useful to put boilerplate or even a full program that the '
            'student should modify. It is possible to configure a global '
            'per-language boilerplate and leave this field blank.'
        ),
    )

    class Meta:
        verbose_name = _('placeholder')
        verbose_name_plural = _('placeholders')


@register_parent_prefetch
class CodingIoQuestion(Question):
    """
    CodeIo questions evaluate source code and judge them by checking if the
    inputs and corresponding outputs match an expected pattern.
    """

    class Meta:
        verbose_name = _('Programming question (IO-based)')
        verbose_name_plural = _('Programming questions (IO-based)')

    num_pre_tests = models.PositiveIntegerField(
        _('# of pre-test examples'),
        default=3,
        validators=[validators.positive_integer_validator],
        help_text=_(
            'The desired number of test cases that will be computed after '
            'comparing the iospec template with the correct answer. This is '
            'only a suggested value and will only be applied if the response '
            'template uses input commands to generate random input.'),
    )
    pre_tests_source = models.TextField(
        _('response template'),
        blank=True,
        validators=[validators.iospec_source_validator],
        help_text=_(
            'Template used to grade I/O responses. See '
            'http://pythonhosted.org/iospec for a complete reference on the '
            'template format.'),
    )
    num_post_tests = models.PositiveIntegerField(
        _('# of post-test examples'),
        validators=[validators.positive_integer_validator],
        default=20
    )
    post_tests_source = models.TextField(
        _('response template (post evaluation)'),
        validators=[validators.iospec_source_validator],
        blank=True,
        help_text=_(
            'These tests are used only in a second round of corrections and is '
            'not immediately shown to users.'),
    )
    test_state_hash = models.CharField(
        max_length=32,
        blank=True,
        help_text=_('A hash to keep track of iospec sources updates.'),
    )
    timeout = models.FloatField(
        _('timeout in seconds'),
        validators=[validators.timeout_validator],
        blank=True,
        default=1.0,
        help_text=_(
            'Defines the maximum runtime the grader will spend evaluating '
            'each test case.'
        ),
    )
    default_placeholder = models.TextField(
        _('placeholder'),
        blank=True,
        help_text=_('Default placeholder message that is used if it is not '
                    'defined for the given language. This will appear as a '
                    'block of comment in the beginning of the submission.')
    )
    language = models.ForeignKey(
        ProgrammingLanguage,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_(
            'Programming language associated with question. Leave it blank in '
            'order to accept submissions in any programming language. This '
            'option should be set only for questions that tests specific '
            'programming languages constructs or require techniques that only '
            'make sense for specific programming languages.'
        ),
    )

    # Fields for storing the results of an async post-validation.
    error_field = models.CharField(max_length=20, blank=True)
    error_message = models.TextField(blank=True)
    ignore_programming_errors = models.BooleanField(
        default=False,
        help_text=_(
            'Mark this if you want to ignore programming errors this time. It '
            'will ignore errors once, but you still have to fix the source '
            'of those errors to make the question become operational.'
        )
    )

    __answers = ()
    _iospec_expansion_is_dirty = False

    @property
    def pre_tests(self):
        try:
            return self._pre_tests
        except AttributeError:
            self._pre_tests = parse_iospec(self.pre_tests_source)
            return self._pre_tests

    @pre_tests.setter
    def pre_tests(self, value):
        self._pre_tests = value
        self.pre_tests_source = value.source()

    @pre_tests.deleter
    def pre_tests(self):
        try:
            del self._pre_tests
        except AttributeError:
            pass

    @property
    def post_tests(self):
        try:
            return self._post_tests
        except AttributeError:
            if self.post_tests_source:
                post_tests = parse_iospec(self.post_tests_source)
            else:
                post_tests = IoSpec()
            self._post_tests = ejudge.combine_iospec(
                self.pre_tests, post_tests)
            return self._post_tests

    @post_tests.setter
    def post_tests(self, value):
        pre_tests = self.pre_tests
        value = IoSpec([test for test in value if test not in pre_tests])
        self._post_tests = ejudge.combine_iospec(self.pre_tests, value)
        self.post_tests_source = value.source()

    @post_tests.deleter
    def post_tests(self):
        try:
            del self._post_tests
        except AttributeError:
            pass

    submission_class = CodingIoSubmission

    def submit(self, request, language=None, **kwargs):
        # Cannot set language if question specifies a required lnaguage
        if language and self.language and language != self.language:
            args = language, self.language
            raise ValueError('cannot set language: %r != %r' % args)

        language = self.language or language
        language = get_programming_language(language)
        return super().submit(request, language=language, **kwargs)

    def load_post_file_data(self, file_data):
        fake_post = super().load_post_file_data(file_data)
        fake_post['pre_tests_source'] = self.pre_tests_source
        fake_post['post_tests_source'] = self.post_tests_source
        return fake_post

    def get_current_test_state(self, update=False):
        """
        Return a current TestState object synchronized with the current
        pre and post tests.

        It raises a ValidationError if an error is encountered during the
        recreation of the test state.
        """

        hash = self.test_state_hash

        try:
            return TestState.objects.get(question=self, hash=hash)
        except TestState.DoesNotExist:
            pre_tests = self.pre_tests
            post_tests = self.post_tests

            def expand(x):
                result = ExpandTests.expand_tests(self, x)
                ExpandTests.check_expansions_with_all_programs(self, result)
                return result

            pre_source = expand(pre_tests).source()
            post_source = expand(post_tests).source()

            return TestState.objects.create(
                question=self,
                hash=hash,
                pre_tests_source=self.pre_tests_source,
                post_tests_source=self.post_tests_source,
                pre_tests_source_expansion=pre_source,
                post_tests_source_expansion=post_source,
            )

    def get_expanded_pre_tests(self):
        """
        Return an IoSpec object with the result of pre tests expansions.
        """

        state = self.get_current_test_state()
        source = state.pre_tests_source_expansion
        return parse_iospec(source)

    def get_expand_post_tests(self):
        """
        Return an IoSpec object with the result of post tests expansions.
        """

        state = self.get_current_test_state()
        source = state.post_tests_source_expansion
        return parse_iospec(source)

    def __expand_tests_to_source(self, tests):
        """
        Return the source of a iospec object full expansion.

        Similar to .expand_tests(), but return a string with the source code
        expansion.
        """

        if tests is None:
            return ''
        return self._expand_tests(tests)

    # Code runners
    def check_with_code(self, source, tests, language=None, timeout=None):
        """
        Wrapped version of check_with_code() that uses question's own timeout
        and language as default.
        """

        language = get_programming_language(language or self.language)
        timeout = timeout or self.timeout
        ejudge.check_with_code(source, tests, language, timeout)

    def run_code(self, source, tests, language=None, timeout=None):
        """
        Wrapped version of run_code() that uses question's own timeout
        and language as default.
        """

        language = get_programming_language(language or self.language)
        timeout = timeout or self.timeout
        return ejudge.run_code(source, tests, language, timeout)

    def grade_code(self, source, inputs, language=None, timeout=None):
        """
        Wrapped version of grade_code() that uses question's own timeout
        and language as default.
        """

        language = get_programming_language(language or self.language)
        timeout = timeout or self.timeout
        return ejudge.grade_code(source, inputs, language, timeout)

    def expand_from_code(self, source, inputs, language=None, timeout=None):
        """
        Wrapped version of expand_from_code() that uses question's own timeout
        and language as default.
        """

        language = get_programming_language(language or self.language)
        timeout = timeout or self.timeout
        return ejudge.expand_from_code(source, inputs, language, timeout)

    # Saving & validation
    def save(self, *args, **kwargs):
        if not self.author_name and self.owner:
            name = self.owner.get_full_name() or self.owner.username
            email = self.owner.email
            self.author_name = '%s <%s>' % (name, email)

        super().save(*args, **kwargs)

    @lazy
    def _validation(self):
        return Validation

    def clean(self):
        return self._validation.clean(self)

    def full_clean(self, *args, **kwargs):
        return self._validation.full_clean(self, *args, **kwargs)

    def full_clean_expansions(self):
        return self._validation.full_clean_expansions(self)

    def full_clean_answer_keys(self):
        return self._validation.full_clean_answer_keys(self)

    def full_clean_all(self, *args, **kwargs):
        return self._validation.full_clean_all(self, *args, **kwargs)

    def schedule_validation(self):
        return self._validation.schedule_validation(self)

    def validate_tests(self):
        return self._validation.validate_tests(self)

    def _expand_from_answer_keys(self):
        # If the source requires expansion, we have to check all answer keys
        # to see if one of them defines a valid source and compute the expansion
        # from this source. All languages must produce the same expansion,
        # otherwise it is considered to be an error.
        #
        # If no answer key is available, leave pre_tests_expanded_source blank
        assert self.pre_tests_expanded is not None
        assert self.post_tests_expanded is not None
        pre, post = self.pre_tests_expanded, self.post_tests_expanded

        useful_keys = list(self.answers_with_code())
        if useful_keys:
            ex_pre = pre.copy()
            ex_pre.expand_inputs(self.number_of_pre_expansions)
            ex_post = post.copy()
            ex_post.expand_inputs(self.number_of_post_expansions)
            pre_list = self.answers.expand_all(ex_pre)
            post_list = self.answers.expand_all(ex_post)

            if len(pre_list) == len(post_list) == 1:
                ex_pre = pre_list[0]
                ex_post = post_list[0]
            else:
                def validate(L, field):
                    first, tail = L
                    for i, elem in enumerate(tail, 1):
                        if first == elem:
                            continue

                        lang1 = useful_keys[0].language
                        lang2 = useful_keys[i].language
                        first.language = lang1
                        elem.language = lang2
                        self.clear_tests()
                        raise validators.inconsistent_testcase_error(first,
                                                                     elem,
                                                                     field)

                validate(pre_list, 'pre_tests_expanded_source')
                validate(post_list, 'post_tests_expanded_source')
                ex_pre, ex_post = pre_list[0], post_list[0]

            # Update values
            self.pre_tests_expanded = ex_pre
            self.pre_tests_expanded_source = ex_pre.source()
            self.post_tests_expanded = ex_pre
            self.post_tests_expanded_source = ex_post.source()

        return self._validation._expand_from_answer_keys(self)

    # Data access

    @lazy
    def _data_access(self):
        return DataAccess

    def get_placeholder(self, language=None):
        return self._data_access.get_placeholder(self, language)

    def get_reference_source(self, language=None):
        return self._data_access.get_reference_source(self, language)

    def filter_user_submission_payload(self, request, payload):
        return self._data_access.filter_user_submission_payload(self, request, payload)

    # Access answer key queryset
    def answers_with_code(self):
        """
        Filter only answers that define a program.
        """

        return self.answers.exclude(source='')

    def run_post_grading(self, **kwargs):
        """
        Runs post tests for all submissions made to this question.
        """

        for response in self.responses.all():
            response.run_post_grading(tests=self.post_tests_expanded, **kwargs)
        self.closed = True
        self.save()

    # Serving pages and routing
    template = 'questions/coding_io/detail.jinja2'
    template_submissions = 'questions/coding_io/submissions.jinja2'
    template_statistics = 'questions/coding_io/statistics.jinja2'
    template_debug = 'questions/coding_io/debug.jinja2'

    def get_context(self, request, *args, **kwargs):
        context = dict(super().get_context(request, *args, **kwargs),
                       form=True)

        # Select default mode for the ace editor
        if self.language:
            context['default_mode'] = self.language.ace_mode()
        else:
            context['default_mode'] = get_config('CODESCHOOL_DEFAULT_ACE_MODE',
                                                 'python')

        # Enable language selection
        if self.language is None:
            context['select_language'] = True
            context['languages'] = ProgrammingLanguage.supported.all()
        else:
            context['select_language'] = False

        return context

    def serve_ajax_submission(self, client, source=None, language=None,
                              **kwargs):
        """
        Handles student responses via AJAX and a bricks program.
        """

        # User must choose language
        if not language or language == '-----':
            if self.language is None:
                fmt = _('Error'), _('Please select the correct language')
                client.dialog(
                    '<p class="dialog-text"><h2>%s</h2><p>%s</p></p>' % fmt
                )
                return None
            language = self.language
        else:
            language = get_programming_language(language)

        return super().serve_ajax_submission(
            client=client,
            language=language,
            source=source,
        )

    @bricks.rpc.route(r'^placeholder/$')
    def route_placeholder(self, request, language):
        """
        Return the placeholder code for some language.
        """

        return self.get_placehoder(language)

    #
    # Actions
    #
    def regrade_post(self):
        """
        Regrade all submissions using the post tests.
        """

        self.responses.regrade_with(self.post_tests_expanded)

    def action_expand_tests(self, client, *args, **kwargs):
        self._expand_tests()
        pre = escape(self.pre_tests_expanded_source)
        post = escape(self.post_tests_expanded_source)
        client.dialog('<h2>Pre-tests</h2><pre>%s</pre>'
                      '<h2>Post-test</h2><pre>%s</pre>' % (pre, post))

    def action_grade_with_post_tests(self, client, *args, **kwargs):
        self.regrade_post()
        client.dialog('<p>Successful operation!</p>')


class ExpandTests(object):
    """
    Expand tests from program and check it
    """

    @classmethod
    def expand_tests(cls, question, tests: IoSpec) -> IoSpec:
        """
        Expand tests and return a new expanded IoSpec object.
        """

        if tests.is_simple:
            return tests.copy()

        # Check if result is usable after a simple expansion
        tests = tests.copy()
        tests.expand_inputs()
        if tests.is_simple:
            return tests

        # Further expansion requires a reference program to automatically
        # compute all the inputs and outputs
        qs = question.answers_with_code()
        if qs:
            language = qs.first().language
        else:
            raise ValidationError(_(
                'No program was provided to expand the given test cases.'
            ))

        return ExpandTests.expand_tests_from_program(question, tests, language)

    @classmethod
    def expand_tests_from_program(cls, question, tests: IoSpec, language=None):
        """
        Uses source code from source code reference in the provided language
        to expand tests.
        """

        language = get_programming_language(language)
        answer_key = question.answers.get(language=language)

        if not answer_key.source:
            raise ValueError('cannot expand from %s: no program set' % language)

        source = answer_key.source

        if tests.is_simple:
            return tests.copy()

        if tests.is_standard_test_case:
            tests = tests.copy()
            tests.expand_inputs()

            if tests.is_simple:
                return tests

        return question.run_code(source, tests, language)

    @classmethod
    def check_expansions_with_all_programs(cls, question, tests: IoSpec):
        """
        Test if source code was expanded in expectancy of what the iospec tests
        provides.

        Remember to expand all commands from the given iospec otherwise each
        program may be run with a different set of inputs.
        """

        answers = list(question.answers_with_code())

        # We can get away with providing no checker program if the tests are
        # simple.
        if not answers and tests.is_expanded:
            return

        # Other cases require more work: first we expand for each possible
        # language. Collect tuples of (expansion, language)
        languages = [answer.language for answer in answers]
        first, *tail = [
            (ExpandTests.expand_tests_from_program(question, tests, language), language)
            for language in languages]

        # All expansions should be equal.
        for expansion in tail:
            if expansion[0] != first[0]:
                raise RuntimeError('different expansions yielded different ')

        question.check_with_code(answers[0].source, tests, answers[0].language,
                                 question.timeout)
        return first[0]
