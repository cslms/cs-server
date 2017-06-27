from django.utils.functional import cached_property
from django.utils.text import ugettext_lazy as _
from wagtail.utils.decorators import cached_classmethod
from wagtail.wagtailadmin.edit_handlers import ObjectList, TabbedInterface
from wagtail.wagtailcore.models import Page

WAGTAIL_ADMIN_CLASSES = {}


class WagtailAdminMeta:

    def __init__(self, model=None, abstract=False):
        self.model = model
        self.abstract = abstract


class WagtailAdminBase(type):

    def __new__(cls, name, bases, ns):
        meta = ns.pop('Meta', None)
        meta_ns = (
            {k: v for k, v in vars(meta).items() if not k.startswith('_')}
            if meta else {}
        )
        ns['_meta'] = WagtailAdminMeta(**meta_ns)
        return type.__new__(cls, name, bases, ns)

    def __init__(cls, name, bases, ns):
        super().__init__(name, bases, ns)
        cls._expand_all_panels()

        # Register model
        if cls._meta.model is None and not cls._meta.abstract:
            raise TypeError('must define a model for concrete class')
        elif cls._meta.model:
            WAGTAIL_ADMIN_CLASSES[cls._meta.model] = cls

    def _expand_all_panels(cls):
        for attr in dir(cls):
            if attr.endswith('_panels'):
                value = expand_panel(cls, attr)
                setattr(cls, attr, value)


def expand_panel(cls, attr):
    """
    Expand the list of panels finding any ellipsis object and substituting it
    by the superclass panels.
    """

    panels = getattr(cls, attr)
    if ... in panels:
        panels = list(panels)
        idx = panels.index(...)
        base = super(cls, cls)
        super_panels = getattr(base, attr)
        pre = panels[:idx]
        post = panels[idx + 1:]
        panels = pre + list(super_panels) + post
    return panels


class WagtailAdmin(metaclass=WagtailAdminBase):

    class Meta:
        abstract = True

    content_panels = list(Page.content_panels)
    promote_panels = list(Page.promote_panels)
    settings_panels = list(Page.settings_panels)

    @cached_property
    def content_tab(self):
        return _('Content'), self.content_panels

    @cached_property
    def promote_tab(self):
        return _('Promote'), self.promote_panels

    @cached_property
    def settings_tab(self):
        return _('Settings'), self.settings_panels, {'classname': 'settings'}

    @cached_property
    def tabs(self):
        return [
            self.content_tab,
            self.promote_tab,
            self.settings_tab,
        ]

    def get_edit_handler(self):
        """
        Get the EditHandler to use in the Wagtail admin when editing this page type.
        """
        if hasattr(self, 'edit_handler'):
            return self.edit_handler.bind_to_model(self)

        # construct a TabbedInterface made up of content_panels, promote_panels
        # and settings_panels, skipping any which are empty
        tabs = []

        for tab in self.tabs:
            title, content, *args = tab
            kwargs = args[0] if args else {}
            tabs.append(ObjectList(content, heading=title, **kwargs))

        model = self._meta.model
        EditHandler = TabbedInterface(tabs,
                                      base_form_class=model.base_form_class)
        return EditHandler.bind_to_model(model)


class DecoupledAdminPage(Page):

    class Meta:
        abstract = True

    @cached_classmethod
    def get_edit_handler(cls):
        if cls in WAGTAIL_ADMIN_CLASSES:
            admin = WAGTAIL_ADMIN_CLASSES[cls]
            return admin().get_edit_handler()
        else:
            return super().get_edit_handler()
