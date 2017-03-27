import logging
from difflib import Differ

import srvice
from annoying.functions import get_config
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _, ugettext as __

from codeschool import models
from codeschool import panels
from codeschool.components.navbar import NavSection
from codeschool.core import get_programming_language
from codeschool.core.models import ProgrammingLanguage
from codeschool.fixes.parent_refresh import register_parent_prefetch
from codeschool.questions.coding_io.models import TestState
from codeschool.questions.models import Question
from codeschool.utils import md5hash_seq
from iospec import parse as parse_iospec, IoSpec
from .submission import CodingIoSubmission
from .. import ejudge
from .. import validators

differ = Differ()
logger = logging.getLogger('codeschool.questions.coding_io')


@register_parent_prefetch
class CodingIoQuestion(Question):
    """
    CodeIo questions evaluate source code and judge them by checking if the
    inputs and corresponding outputs match an expected pattern.
    """

    class Meta:
        verbose_name = _('Programming question (IO-based)')
        verbose_name_plural = _('Programming questions (IO-based)')

    EXT_TO_METHOD_CONVERSIONS = dict(
        Question.EXT_TO_METHOD_CONVERSIONS,
        md='markio',
    )

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
            self._post_tests = ejudge.combine_iospec(self.pre_tests, post_tests)
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

    def load_post_file_data(self, file_data):
        fake_post = super().load_post_file_data(file_data)
        fake_post['pre_tests_source'] = self.pre_tests_source
        fake_post['post_tests_source'] = self.post_tests_source
        return fake_post

    # Expanding and controlling the tests state
    def has_test_state_changed(self):
        """
        Return True if test state has changed.
        """

        return self.test_state_hash == compute_test_state_hash(self)

    def get_current_test_state(self, update=False):
        """
        Return a current TestState object synchronized with the current
        pre and post tests.

        It raises a ValidationError if an error is encountered during the
        recreation of the test state.
        """

        if update:
            hash = compute_test_state_hash(self)
        else:
            hash = self.test_state_hash

        try:
            return TestState.objects.get(question=self, hash=hash)
        except TestState.DoesNotExist:
            pre_tests = self.pre_tests
            post_tests = self.post_tests

            def expand(x):
                result = expand_tests(self, x)
                check_expansions_with_all_programs(self, result)
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
        self.test_state_hash = compute_test_state_hash(self)

        if not self.author_name and self.owner:
            name = self.owner.get_full_name() or self.owner.username
            email = self.owner.email
            self.author_name = '%s <%s>' % (name, email)

        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        if self.has_test_state_changed() or self.has_code_changed():
            logger.debug('%r: recomputing tests' % self.title)
            self.schedule_validation()

    def full_clean(self, *args, **kwargs):
        if self.__answers:
            self.answers = self.__answers
        super().full_clean(*args, **kwargs)

    def full_clean_expansions(self):
        self.get_current_test_state(update=True)

    def full_clean_answer_keys(self):
        """
        Performs a full_clean() validation step on all answer key objects.
        """

        for key in self.answers.all():
            try:
                key.question = self
                key.full_clean()
            except ValidationError as ex:
                raise validators.invalid_related_answer_key_error(key, ex)

    def full_clean_all(self, *args, **kwargs):
        self.full_clean(*args, **kwargs)
        self.full_clean_answer_keys()
        self.full_clean_expansions()

    def schedule_validation(self):
        """
        Schedule full validation to be performed in the background.

        This executes the full_clean_code() method
        """

        print('scheduling full code validation... (we are now executing on the'
              'foreground).')
        self.mark_invalid_code_fields()

    def mark_invalid_code_fields(self):
        """
        Performs a full code validation with .full_clean_code() and marks all
        errors found in the question.
        """

        return
        try:
            self.full_clean(force_expansions=True)
        except ValidationError as ex:
            print(ex)
            print(dir(ex))
            raise

    def validate_tests(self):
        """
        Triggered when (pre|post)_test_source changes or on the first time the
        .clean() method is called.
        """

        # Check if new source is valid
        for attr in ['pre_tests_source', 'post_tests_source']:
            try:
                source = getattr(self, attr)
                if source:
                    iospec = parse_iospec(source)
                else:
                    iospec = None
                setattr(self, attr[:-7], iospec)
            except Exception as ex:
                self.clear_tests()
                raise ValidationError(
                    {attr: _('invalid iospec syntax: %s' % ex)}
                )

        # Computes temporary expansions for all sources. A second step may be
        # required in which we use the reference source in answer key to further
        # expand iospec data structures
        iospec = self.pre_tests.copy()
        iospec.expand_inputs(self.number_of_pre_expansions)
        self.pre_tests_expanded = iospec

        if self.pre_tests_source and self.post_tests_source:
            iospec = ejudge.combine_iospecs(self.pre_tests, self.post_tests)
        elif self.post_tests_source:
            iospec = self.post_tests.copy()
        elif self.pre_tests_source:
            iospec = self.pre_tests.copy()
        else:
            raise ValidationError(_(
                'either pre_tests_source or post_tests_source must be given!'
            ))
        iospec.expand_inputs(self.number_of_post_expansions)
        # assert len(iospec) >= self.number_of_expansions, iospec
        self.post_tests_expanded = iospec

        if self.pre_tests_expanded.is_expanded and \
                self.post_tests_expanded.is_expanded:
            self.pre_tests_expanded_source = self.pre_tests_expanded.source()
            self.post_tests_expanded_source = self.post_tests_expanded.source()

        else:
            self._expand_from_answer_keys()

        # Iospec is valid: save the hash
        self.tests_state_hash = self.current_tests_hash

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
                    first, *tail = L
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

    # Data access
    def get_placeholder(self, language=None):
        """
        Return the placeholder text for the given language.
        """

        key = self.answers.get(language or self.language, None)
        if key is None:
            return self.default_placeholder
        return key.placeholder

    def get_reference_source(self, language=None):
        """
        Return the reference source code for the given language or None, if no
        reference is found.
        """

        if language is None:
            language = self.language
        qs = self.answers.all().filter(
            language=get_programming_language(language))
        if qs:
            return qs.get().source
        return ''

    def get_submission_kwargs(self, request, kwargs):
        return dict(language=kwargs['language'], source=kwargs['source'])

    # Access answer key queryset
    def answers_with_code(self):
        """
        Filter only answers that define a program.
        """

        return self.answers.exclude(source='')

    def has_code_changed(self):
        """
        True if some answer source for a valid code has changed.
        """

        keys = self.answers_with_code()
        for key in keys:
            if key.has_changed_source():
                return True
        return False

    # Actions
    def submit(self, user_or_request, language=None, **kwargs):
        if language and self.language:
            if language != self.language:
                args = language, self.language
                raise ValueError('cannot set language: %r != %r' % args)
        if self.language:
            language = self.language
        language = get_programming_language(language)
        return super().submit(user_or_request, language=language, **kwargs)

    def run_post_grading(self, **kwargs):
        """
        Runs post tests for all submissions made to this question.
        """

        for response in self.responses.all():
            response.run_post_grading(tests=self.post_tests_expanded, **kwargs)
        self.closed = True
        self.save()

    def nav_section_for_activity(self, request):
        url = self.get_absolute_url
        section = NavSection(__('Question'), url(),
                             title=__('Back to question'))
        if self.user_can_edit(request.user):
            section.add_link(__('Edit'), self.get_admin_url(),
                             title=__('Edit question'))
        section.add_link(__('Submissions'), url('submissions'),
                         title=__('View your submissions'))
        return section

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
        Handles student responses via AJAX and a srvice program.
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

    @srvice.route(r'^placeholder/$')
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

    # Wagtail admin
    content_panels = Question.content_panels[:]
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
    settings_panels = Question.settings_panels + [
        panels.MultiFieldPanel([
            panels.FieldPanel('language'),
            panels.FieldPanel('timeout'),
        ], heading=_('Options'))
    ]


def compute_test_state_hash(question):
    source_hashes = question.answers.values_list('source_hash', flat=True)
    return md5hash_seq([
        question.pre_tests_source,
        question.post_tests_source,
        '%x%x%f' % (question.num_pre_tests, question.num_post_tests,
                    question.timeout),
        '\n'.join(source_hashes),
    ])


#
# Utility functions
#
def expand_tests(question, tests: IoSpec) -> IoSpec:
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

    return expand_tests_from_program(question, tests, language)


def expand_tests_from_program(question, tests: IoSpec, language=None):
    """
    Uses source code from source code reference in the provided language
    to expand tests.
    """

    language = get_programming_language(language)
    answer_key = question.answers.get(language=language)

    if not answer_key.source:
        raise ValueError('cannot expand from %s: no program set' % language)

    source = answer_key.source
    language_ref = language.ejudge_ref()

    if tests.is_simple:
        return tests.copy()

    if tests.is_standard_test_case:
        tests = tests.copy()
        tests.expand_inputs()

        if tests.is_simple:
            return tests

    return question.run_code(source, tests, language)


def check_expansions_with_all_programs(question, tests: IoSpec):
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
    first, *tail = [(expand_tests_from_program(question, tests, language), language)
                    for language in languages]

    # All expansions should be equal.
    for expansion in tail:
        if expansion[0] != first[0]:
            raise RuntimeError('different expansions yielded different ')

    question.check_with_code(answers[0].source, tests, answers[0].language,
                             question.timeout)
    return first[0]
