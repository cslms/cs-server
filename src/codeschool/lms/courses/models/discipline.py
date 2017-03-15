from django.utils.translation import ugettext_lazy as _

from codeschool import models


class Discipline(models.TimeStampedModel):
    """
    Represents an academic discipline.
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(_('short name'))
    description = models.RichTextField(blank=True)
    syllabus = models.RichTextField(blank=True)
