import model_reference
import srvice
from django.db import transaction
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from codeschool import mixins
from codeschool import models, panels
from ..types.score_map import ScoreTable, ScoreMap


class ScoreBoardMixin(models.RoutablePageMixin,
                      models.Page):
    """
    Basic ScoreBoard functionality.
    """

    class Meta:
        abstract = True

    def score_board(self, info=None):
        """
        Return a ScoreTable object with the grades of all students from the
        sub-page activities.
        """

        info = info or 'points'
        if info not in ['points', 'grade', 'stars', 'score']:
            raise ValueError('invalid info: %r' % info)

        board = ScoreTable(name=self.title)
        for page in self.get_children():
            col = page.specific.score_board(info=info)
            board.add_column(col)
        return board

    @srvice.route(r'^score-board/$')
    def serve_score_board(self, client):
        board = self.score_board()
        board.sort()
        board.add_total('total', method='sum')
        client.dialog(html=str(board))

    @models.route(r'^score-board[\.]csv/$')
    def serve_score_board_csv(self, request):
        board = self.score_board()
        board.sort()
        board.add_total('total', method='sum')
        return HttpResponse(board.to_csv())


class ActivityListQuerySet(models.PageQuerySet):

    def create_subpage(self, parent, **kwargs):
        """
        Return a new page as a child of the given parent page.
        """

        return self.model.create_subpage(parent, **kwargs)


class _ActivityListManager(models.PageManager):

    def main(self):
        """
        Return the main ActivityList for the website.
        """

        return model_reference.load('root-page', model=ActivityList)


ActivityListManager = _ActivityListManager.from_queryset(ActivityListQuerySet)


class ActivityList(ScoreBoardMixin,
                   mixins.ShortDescriptionPage,
                   models.Page):
    """
    A list of ActivitySections.
    """

    class Meta:
        verbose_name = _('list of activities')
        verbose_name_plural = _('lists of activities')

    BEGINNER_SECTIONS = [
        'basic', 'conditionals', 'loops', 'functions', 'files', 'lists'
    ]
    INTERMEDIATE_SECTIONS = [
        # 'classes', 'iterators',  # whatnot...
    ]
    MARATHON_SECTIONS = [
        # 'graphs', 'lists', 'strings',
    ]

    @classmethod
    def create_subpage(cls, parent=None, **kwargs):
        """
        Create a new ActivityList using the given keyword arguments under the
        given parent page. If no parent is chosen, uses the main Wagtail root
        page.
        """

        kwargs.update(
            title=_('Activities'),
            short_description=kwargs.get('short_description',
                                         _('List of activities.')),
            slug='activities',
        )
        parent = parent or model_reference.load('root-page')
        new = cls(**kwargs)
        print('parent', parent)
        parent.add_child(instance=new)
        new.save()
        return new

    @classmethod
    def from_template(cls, template, parent=None):
        """
        Creates a new instance from the given template.

        Valid templates are:
            programming-beginner
                Basic sections in a beginner programming course.
            programming-intermediate
                Sections for a second course on programming course.
            programming-marathon
                Sections for a marathon based course.
        """

        with transaction.atomic():
            new = cls.create_subpage(parent)
            new.update_from_template(template)
            return new

    def update_from_template(self, template):
        """
        Updates activity list from template.
        """

        sections = {
            'programming-beginner': self.BEGINNER_SECTIONS,
            'programming-intermediate': self.INTERMEDIATE_SECTIONS,
            'programming-marathon': self.MARATHON_SECTIONS,
        }.get(template, None)

        if sections is None:
            raise ValueError('invalid template name: %r' % template)

        for section in sections:
            self.add_standard_section(section)

    def add_standard_section(self, name):
        """
        Adds a standard section to activity list, if it does not exist.
        """

        if self.get_children().filter(slug=name).count() == 0:
            ActivitySection.from_template(name, self)

    def score_board(self, info=None):
        board = ScoreTable(name=self.title)
        for page in self.get_children():
            col = page.specific.score_board_total()
            board.add_column(col)
        return board

    # Serving pages
    template = 'lms/activities/list.jinja2'

    def get_context(self, request, *args, **kwargs):
        return dict(
            super().get_context(request, *args, **kwargs),
            object_list=[obj.specific for obj in self.get_children()]
        )

    # Wagtail admin
    subpage_types = ['ActivitySection']


class ActivitySection(ScoreBoardMixin,
                      mixins.ShortDescriptionPage,
                      models.Page):
    """
    List of activities.
    """

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')

    material_icon = models.CharField(
        _('Optional icon'),
        max_length=20,
        default='help',
    )
    objects = ActivityListManager()

    @property
    def activities(self):
        return [x.specific for x in self.get_children()]

    # Special template constructors
    @classmethod
    def create_subpage(cls, parent=None, **kwargs):
        """
        Create a new ActivitySection using the given keyword arguments under the
        given parent page. If no parent is chosen, uses the "main-question-list"
        reference.
        """

        parent = parent or model_reference.load('main-question-list')
        new = cls(**kwargs)
        parent.add_child(instance=new)
        new.save()
        return new

    @classmethod
    def from_template(cls, template, parent=None):
        """
        Creates a new instance from the given template.

        Valid templates are:
            basic
                Very basic beginner IO based problems. First contact with
                programming.
            conditionals
                Simple problems based on if/else flow control.
            loops
                Problems that uses for/while loops.
            functions
                Problems that uses functions.
            files
                Reading and writing files.
            lists
                Linear data structures such as lists and arrays.
        """

        try:
            factory = getattr(cls, '_template_%s' % template)
            return factory(parent)
        except AttributeError:
            raise ValueError('invalid template name: %r' % template)

    @classmethod
    def _template_basic(cls, parent):
        return cls.create_subpage(
            parent,
            title=_('Basic'),
            short_description=_('Elementary programming problems.'),
            slug='basic',
            material_icon='insert_emoticon',
        )

    @classmethod
    def _template_conditionals(cls, parent):
        return cls.create_subpage(
            parent,
            title=_('Conditionals'),
            short_description=_('Conditional flow control (if/else).'),
            slug='conditionals',
            material_icon='code',
        )

    @classmethod
    def _template_loops(cls, parent):
        return cls.create_subpage(
            parent,
            title=_('Loops'),
            short_description=_('Iterations with for/while commands.'),
            slug='loops',
            material_icon='loop',
        )

    @classmethod
    def _template_functions(cls, parent):
        return cls.create_subpage(
            parent,
            title=_('Functions'),
            short_description=_('Organize code using functions.'),
            slug='functions',
            material_icon='functions',
        )

    @classmethod
    def _template_files(cls, parent):
        return cls.create_subpage(
            parent,
            title=_('Files'),
            short_description=_('Open, process and write files.'),
            slug='files',
            material_icon='insert_drive_file',
        )

    @classmethod
    def _template_lists(cls, parent):
        return cls.create_subpage(
            parent,
            title=_('Lists'),
            short_description=_('Linear data structures.'),
            slug='lists',
            material_icon='list',
        )

    def save(self, *args, **kwargs):
        if self.title is None:
            self.title = _('List of activities')
        if self.slug is None:
            self.slug = 'activities'
        super().save(*args, **kwargs)

    def score_board_total(self):
        """
        Return a score board mapping with the total score for each user.
        """

        board = self.score_board()
        scores = ScoreMap(self.title)
        for k, L in board.items():
            scores[k] = sum(L)
        return scores

    # Serving pages
    template = 'lms/activities/section.jinja2'

    def get_context(self, request, *args, **kwargs):
        return dict(
            super().get_context(request, *args, **kwargs),
            object_list=[obj.specific for obj in self.get_children()]
        )

    # Wagtail Admin
    parent_page_types = [ActivityList]
    content_panels = mixins.ShortDescriptionPage.content_panels + [
        panels.FieldPanel('material_icon')
    ]


@model_reference.factory('main-question-list')
def make_main_activity_list():
    """
    Creates the default site-wide activity list. Other activity lists may
    appear under different sections in the site.
    """

    parent_page = model_reference.load('root-page')
    try:
        return ActivityList.objects.get(path__startswith=parent_page.path,
                                        slug='questions')
    except ActivityList.DoesNotExist:
        activity_list = ActivityList(
            title=_('Questions'),
            slug='questions',
        )
        return parent_page.add_child(instance=activity_list)
