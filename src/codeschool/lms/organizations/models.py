from django.utils.translation import ugettext_lazy as _

from codeschool import models


class DescriptiveModel(models.TimeStampedModel):
    """
    Abstract Base Class for models with slug/name/description fields.

    Slug is used as a primary key.
    """

    slug = models.CodeschoolSlugField(
        _('Slug'),
        primary_key=True,
    )
    name = models.CodeschoolNameField(
        _('Name'),
    )
    description = models.CodeschoolDescriptionField(
        _('Description'),
        blank=True,
        help_text=_(
            'A one-phrase description used in listings.'
        )
    )

    class Meta:
        abstract = True

    def __str__(self):
        return '%s (%s)' % (self.name, self.slug)


class Organization(DescriptiveModel):
    """
    A basic organizational entity in a an school or university.

    Can be an department, a campus, a specific branch or represent the whole
    institution itself.
    """


class Discipline(DescriptiveModel):
    """
    An academic discipline.
    """

    faculty = models.ForeignKey(
        'Organization',
        blank=True
    )
    school_id = models.CharField(
        max_length=50,
        blank=True
    )
    since = models.DateField(blank=True, null=True)

    # These were modeled as in https://matriculaweb.unb.br/, which is not
    # particularly good. In the future we want structured data types.
    syllabus = models.RichTextField(blank=True)
    program = models.RichTextField(blank=True)
    bibliography = models.RichTextField(blank=True)
