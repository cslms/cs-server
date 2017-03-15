"""
Important singleton pages for a codeschool installation.
"""
import model_reference
from django.utils.translation import ugettext_lazy as _
from codeschool import models


class HiddenRoot(models.ProxyPageMixin, models.SinglePageMixin, models.Page):
    """
    A page representing the site's root page
    """

    class Meta:
        proxy = True

    @classmethod
    def get_state(cls):
        return {
            'title': _('Hidden pages'),
            'locked': True,
            'slug': 'hidden'
        }

    @classmethod
    def get_parent(cls):
        return models.Page.objects.get(path='0001')

    parent_page_types = []


class RogueRoot(models.ProxyPageMixin, models.SinglePageMixin, models.Page):
    """
    A page representing the site's root page
    """

    class Meta:
        proxy = True

    @classmethod
    def get_state(cls):
        return {
            'title': _('Rogue pages'),
            'locked': True,
            'slug': 'rogue'
        }

    @classmethod
    def get_parent(cls):
        return HiddenRoot.objects.instance()

    parent_page_types = []


@model_reference.factory('root-page')
def wagtail_root_page():
    return models.Page.objects.get(path='00010001')


@model_reference.factory('rogue-root')
def rogue_root_page():
    return RogueRoot.instance()


@model_reference.factory('hidden-root')
def hidden_root_page():
    return HiddenRoot.instance()
