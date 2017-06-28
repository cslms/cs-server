import model_reference
from django.utils.translation import ugettext_lazy as _

from codeschool import mixins
from codeschool import models
from .managers import ActivitySectionManager
from .mixins import ScoreBoardMixin
from .score_map import ScoreTable, ScoreMap


class ActivityList(ScoreBoardMixin,
                   models.DecoupledAdminPage,
                   models.RoutableViewsPage,
                   mixins.ShortDescriptionPage,
                   models.Page):
    """
    A list of ActivitySections.
    """

    class Meta:
        verbose_name = _('list of activities')
        verbose_name_plural = _('lists of activities')
        app_label = 'activities'

    BEGINNER_SECTIONS = [
        'basic', 'conditionals', 'loops', 'functions', 'files', 'lists'
    ]
    INTERMEDIATE_SECTIONS = [
        # 'classes', 'iterators',  # whatnot...
    ]
    MARATHON_SECTIONS = [
        # 'graphs', 'lists', 'strings',
    ]

    def update_from_template(self, template):
        """
        Updates activity list from template.
        """

        sections = {
            'programming-beginner': self.BEGINNER_SECTIONS,
            'programming-intermediate': self.INTERMEDIATE_SECTIONS,
            'programming-marathon': self.MARATHON_SECTIONS,
        }.get(template)

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


class ActivitySection(ScoreBoardMixin,
                      models.DecoupledAdminPage,
                      models.RoutableViewsPage,
                      mixins.ShortDescriptionPage,
                      models.Page):
    """
    List of activities.
    """

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')
        app_label = 'activities'

    material_icon = models.CharField(
        _('Optional icon'),
        max_length=20,
        default='help',
    )
    objects = ActivitySectionManager()

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

# Import views explicitly until it becomes an app
from . import views
views._loaded = True
