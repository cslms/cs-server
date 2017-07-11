from django.utils.translation import ugettext_lazy as _

from codeschool import models


class ActivityListManager(models.Manager):
    BEGINNER_SECTIONS = [
        'basic', 'conditionals', 'loops', 'functions', 'files', 'lists'
    ]
    INTERMEDIATE_SECTIONS = [
        # 'classes', 'iterators',  # whatnot...
    ]
    MARATHON_SECTIONS = [
        # 'graphs', 'lists', 'strings',
    ]

    def create_lists_from_template(self, template, parent=None):
        """
        Creates a new set of Activity Lists from the given template.

        Valid templates are:
            programming-beginner
                Basic sections in a beginner programming course.
            programming-intermediate
                Sections for a second course on programming course.
            programming-marathon
                Sections for a marathon based course.
        """

        lists = {
            'programming-beginner': self.BEGINNER_SECTIONS,
            'programming-intermediate': self.INTERMEDIATE_SECTIONS,
            'programming-marathon': self.MARATHON_SECTIONS,
        }.get(template)

        if lists is None:
            raise ValueError('invalid template name: %r' % template)

        new = [self.create_from_template(template) for template in lists]
        self.bulk_create(new)
        return new

    def create_from_template(self, template):
        """
        Creates a single ActivityList instance from the given template.

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
            factory = getattr(self, '_template_%s' % template)
            return factory()
        except AttributeError:
            raise ValueError('invalid template name: %r' % template)

    def _template_basic(self):
        return self.model(
            name=_('Basic'),
            short_description=_('Elementary programming problems.'),
            slug='basic',
            icon='insert_emoticon',
        )

    def _template_conditionals(self):
        return self.model(
            name=_('Conditionals'),
            short_description=_('Conditional flow control (if/else).'),
            slug='conditionals',
            icon='code',
        )

    def _template_loops(self):
        return self.model(
            name=_('Loops'),
            short_description=_('Iterations with for/while commands.'),
            slug='loops',
            icon='loop',
        )

    def _template_functions(self):
        return self.model(
            name=_('Functions'),
            short_description=_('Organize code using functions.'),
            slug='functions',
            icon='functions',
        )

    def _template_files(self):
        return self.model(
            name=_('Files'),
            short_description=_('Open, process and write files.'),
            slug='files',
            icon='insert_drive_file',
        )

    def _template_lists(self):
        return self.model(
            name=_('Lists'),
            short_description=_('Linear data structures.'),
            slug='lists',
            icon='list',
        )
