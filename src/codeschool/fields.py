#
# One stop shop for fields.
#
from django.db.models.fields import *  # noqa
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.fields import StreamField, RichTextField, BlockField
from modelcluster.fields import ParentalKey
from annoying.fields import AutoOneToOneField
from picklefield.fields import PickledObjectField
from jsonfield.fields import JSONField
from model_utils.fields import \
    AutoCreatedField, AutoLastModifiedField, MonitorField, SplitField, \
    StatusField
from model_utils import FieldTracker

__all__ = (
    'StreamField', 'RichTextField', 'BlockField', 'ParentalKey',
    'AutoOneToOneField', 'PickledObjectField', 'JSONField',
    'AutoCreatedField', 'AutoLastModifiedField', 'AutoField',
    'MonitorField', 'SplitField', 'FieldTracker', 'CodeschoolDescriptionField',
    'CodeschoolSlugField', 'CodeschoolNameField',
    'CodeschoolShortDescriptionField',
)

#
# Simple factory functions that define default parameters for common fields.
#
_shortdescr = _('short description')


def CodeschoolNameField(verbose=_('name'), max_length=100, **kwargs):  # noqa
    """
    A CharField with default parameters.
    """
    return CharField(verbose, max_length=max_length, **kwargs)


def CodeschoolSlugField(verbose=_('Short name'), **kwargs):  # noqa
    """
    A slug field with default parameters.
    """
    kwargs.setdefault('help_text', _(
        'Unique short name used on URLs.'
    ))
    return SlugField(verbose, **kwargs)


def CodeschoolShortDescriptionField(verbose=_shortdescr, **kwargs):  # noqa
    """
    A CharField with default parameters.
    """
    kwargs.setdefault('help_text', _(
        'A short one-sentence description used in listings.'
    ))
    kwargs.setdefault('max_length', 140)
    return CharField(verbose, **kwargs)


def CodeschoolDescriptionField(verbose=_('Description'), **kwargs):  # noqa
    """
    A RichTextField with default parameters.
    """
    kwargs.setdefault('help_text', _(
        'Long and detailed description.'
    ))
    return RichTextField(verbose, **kwargs)
