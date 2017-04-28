#
# One stop shop for fields.
#
# flake8: noqa
from django.db.models.fields import *
from wagtail.wagtailcore.fields import StreamField, RichTextField, BlockField
#from wagtailmarkdown.fields import MarkdownField
from modelcluster.fields import ParentalKey
from annoying.fields import AutoOneToOneField
from picklefield.fields import PickledObjectField
from django.core.serializers.json import DjangoJSONEncoder as _DjangoJSONEncoder
from django.utils.translation import ugettext_lazy as _
from jsonfield.fields import JSONField
from model_utils.fields import (
    AutoCreatedField, AutoLastModifiedField, MonitorField, SplitField,
    StatusField
)
from model_utils import FieldTracker


#
# Simple factory functions that define default parameters for common fields.
#
def CodeschoolNameField(verbose=_('name'), max_length=100, **kwargs):  # noqa
    """
    Default parameters for the name field.
    """
    return CharField(verbose, max_length=max_length, **kwargs)


def CodeschoolSlugField(verbose=_('Short name'), **kwargs):  # noqa
    """
    Default parameters for the name field.
    """
    kwargs.setdefault('help_text', _(
        'Unique short name used on urls.'
    ))
    return SlugField(verbose, **kwargs)


def CodeschoolDescriptionField(verbose=_('Description'), **kwargs):  # noqa
    """
    Default parameters for the name field.
    """
    return RichTextField(verbose, **kwargs)
