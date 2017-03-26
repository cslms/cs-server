import srvice
from django.core.exceptions import ImproperlyConfigured
from django.http import response
from django.template import TemplateDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render

import codeschool.mixins
from codeschool import blocks
from codeschool import models
from codeschool import panels
from codeschool.lms.activities.models import Activity, Submission, Progress
from codeschool.lms.activities.models.feedback import Feedback
from codeschool.questions.forms import QuestionAdminModelForm


QUESTION_BODY_BLOCKS = [
    ('paragraph', blocks.RichTextBlock()),
    ('heading', blocks.CharBlock(classname='full title')),
    ('markdown', blocks.MarkdownBlock()),
    ('html', blocks.RawHTMLBlock()),
]


class QuestionMeta(type(Activity)):
    CONCRETE_QUESTION_TYPES = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self._meta.abstract:
            self.CONCRETE_QUESTION_TYPES.append(self)


class Question(codeschool.mixins.ShortDescriptionPageMixin,
               Activity, metaclass=QuestionMeta):
    """
    Base abstract class for all question types.
    """

    instant_autograde = True

    class Meta:
        abstract = True
        permissions = (("download_question", "Can download question files"),)

    EXT_TO_METHOD_CONVERSIONS = {'yml': 'yaml'}
    OPTIONAL_IMPORT_FIELDS = ['author_name', 'comments', 'score_value',
                              'star_value']
    base_form_class = QuestionAdminModelForm

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

    # Serve pages
    def get_submission_kwargs(self, request, kwargs):
        return {}

    def get_context(self, request, progress=False, *args, **kwargs):
        context = dict(
            super().get_context(request, *args, **kwargs),
            question=self,
            form_name='response-form',
        )

        if progress:
            context['progress'] = self.responses.response_for_request(request),
        return context

    def get_statistics_context(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['statistics'] = self.get_statistics(request.user)
        return context

    def get_debug_context(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        return context

    def render_from_template(self, category, request, context):
        """
        Fetch template name from explicit configuration or compute the default
        value from the class name
        """

        try:
            template = getattr(self, 'template_%s' % category)
            return render(request, template, context)
        except AttributeError:
            name = self.__class__.__name__.lower()
            if name.endswith('question'):
                name = name[:-8]
            template = 'questions/%s/%s.jinja2' % (category, name)

            try:
                return render(request, template, context)
            except TemplateDoesNotExist:
                raise ImproperlyConfigured(
                    'Model %s must define a template_%s attribute. '
                    'You  may want to extend this template from '
                    '"questions/%s.jinja2"' % (
                        self.__class__.__name__, category, category
                    )
                )

    #
    # Route implementations
    #
    # Wagtail routes do not handle subclasses well and we also do not want to
    # to repeat the correct routing parameters each time a route is subclassed.
    #
    # Subclass thus must override the serve_* methods instead of the route_*
    # versions.
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
            feedback = submission.autograde()
            data = feedback.render_message()
            client.dialog(html=data)
        else:
            client.dialog(html='Your submission is on the correction queue!')

    def serve_list_submissions_page(self, request, *args, **kwargs):
        """
        Renders a user request for the list of submissions.
        """

        submissions = self.submissions\
            .for_user(request.user)\
            .order_by('-created')
        context = self.get_context(request, response=None, *args, **kwargs)
        context['submissions'] = submissions
        context['disable_nav_bar'] = True
        return self.render_from_template('submissions', request, context)

    def serve_statistics_page(self, request, *args, **kwargs):
        """
        Display a page with question statistics.
        """

        context = self.get_statistics_context(request, *args, **kwargs)
        return self.render_from_template('statistics', request, context)

    def serve_debug_page(self, request, *args, **kwargs):
        """
        Display a debug page for site administrators and question owners.
        """
        if request.user != self.owner:
            return response.HttpResponseForbidden()
        context = self.get_debug_context(request, *args, **kwargs)
        return self.render_from_template('debug', request, context)

    #
    # route_* to serve_* mappings
    #
    @srvice.route(r'^submit-response.api/$', name='submit-ajax')
    def route_ajax_submission(self, client, **kwargs):
        return self.serve_ajax_submission(client, **kwargs)

    @models.route(r'^submissions/$', name='list-submissions')
    def route_list_submissions_page(self, request, *args, **kwargs):
        return self.serve_list_submissions_page(request, *args, **kwargs)

    @models.route(r'^statistics/$', name='statistics')
    def route_statistics_page(self, request, *args, **kwargs):
        return self.serve_statistics_page(request, *args, **kwargs)

    @models.route(r'^debug/$', name='debug')
    def route_debug_page(self, request, *args, **kwargs):
        return self.serve_debug_page(request, *args, **kwargs)

    @models.route(r'^leaderboard/$')
    @models.route(r'^social/$')
    def route_page_does_not_exist(self, request):
        return render(request, 'base.jinja2', {
            'content_body': 'The page you are trying to see is not implemented '
                            'yet.',
            'content_title': 'Not implemented',
            'title': 'Not Implemented'
        })

    # Wagtail admin
    subpage_types = []
    content_panels = codeschool.mixins.ShortDescriptionPageMixin.content_panels[:-1] + [
        panels.MultiFieldPanel([
            panels.FieldPanel('import_file'),
            panels.FieldPanel('short_description'),
        ], heading=_('Options')),
        panels.StreamFieldPanel('body'),
        panels.MultiFieldPanel([
            panels.FieldPanel('author_name'),
            panels.FieldPanel('comments'),
        ], heading=_('Optional information'),
            classname='collapsible collapsed'),
    ]


class QuestionMixin:
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

# #
# # Gradebook object (move somewhere else)
# #
# class UserGradebook:
#     def __init__(self, questions, user):
#         self.questions = questions
#         self.user = user
#
#     def __iter__(self):
#         user = self.user
#         for question in self.questions:
#             response = question.get_response(user)
#             attempts = response.num_attempts
#             response.update(force=True)
#             grade = response.final_grade
#             url = question.get_absolute_url()
#             title = escape(question.title)
#             question_link = '<a href="%s">%s</a>' % (url, title)
#             yield (question_link, attempts, '%.1f%%' % grade)
#
#     def render(self):
#         head = _('Question'), _('# attempts'), _('Final grade')
#         lines = [
#             '<table class="gradebook">',
#             '<thead>',
#             '<tr><th>%s</th><th>%s</th><th>%s</th></tr>' % head,
#             '</thead>',
#             '<tbody>',
#         ]
#         for (question, N, grade) in self:
#             line = question, N, grade
#             line = ''.join('<td>%s</td>' % elem for elem in line)
#             line = '<tr>%s</tr>' % line
#             lines.append(line)
#         lines.extend([
#             '</tbody>',
#             '</table>'
#         ])
#         return '\n'.join(lines)
#
#     def __html__(self):
#         return self.render()
#
#     def __str__(self):
#         return self.render()
#
#
# class ClassGradebook:
#     def __init__(self, questions=None, users=None):
#         self.questions = list(questions or self._all_questions())
#         self.users = list(users or self._all_users())
#         self.columns = [q.slug for q in self.questions]
#         self.rows = [self._row(user) for user in self.users]
#
#     def _row(self, user):
#         row = []
#         for question in self.questions:
#             response = question.get_response(
#                 user=user,
#                 context=question.default_context
#             )
#             row.append(response.final_grade)
#         return row
#
#     def _all_users(self):
#         return models.User.objects.exclude(username='AnonymousUser')
#
#     def _all_questions(self):
#         ctypes = question_content_types()
#         return models.Page.objects.filter(content_type__in=ctypes).specific()
#
#     def render(self):
#         head = [_('Student')] + self.columns
#         head = ''.join('<th>%s</th>' % x for x in head)
#         lines = [
#             '<table class="gradebook">',
#             '<thead>',
#             '<tr>%s</tr>' % head,
#             '</thead>',
#             '<tbody>',
#         ]
#         for (user, row) in zip(self.users, self.rows):
#             line = [user.get_full_name() or user.username]
#             line.extend(row)
#             line = ''.join('<td>%s</td>' % x for x in line)
#             line = '<tr>%s</tr>' % line
#             lines.append(line)
#         lines.extend([
#             '</tbody>',
#             '</table>'
#         ])
#         return '\n'.join(lines)
#
#     def render_csv(self):
#         data = [',' + ','.join(self.columns)]
#         for user, row in zip(self.users, self.rows):
#             line = [user.username]
#             line.extend(row)
#             data.append(','.join(map(str, line)))
#         return '\n'.join(data)
#
#     def __str__(self):
#         return self.render()
#
#     def __html__(self):
#         return self.render()
#
#
# def question_content_types():
#     ct_getter = models.ContentType.objects.get
#     return (
#         ct_getter(app_label='cs_questions', model='formquestion'),
#         ct_getter(app_label='cs_questions', model='codingioquestion')
#     )
