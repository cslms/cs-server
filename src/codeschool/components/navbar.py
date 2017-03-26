import pyml
from pyml import nav, a, p, ul, li, hyperlink


class NavSection(pyml.Component):
    """
    Basic NavSection component.
    """

    @property
    def title_element(self):
        if self.href:
            return a(self.name, cls='cs-nav__block-title',
                     attrs=self.title_kwargs)
        else:
            return p(self.name, cls='cs-nav__block-title',
                     attrs=self.title_kwargs)

    def __init__(self, name, href=None, title=None, **kwargs):
        self.links = []
        self.name = name
        self.title_kwargs = {k[6:]: v for k, v in kwargs.items()
                             if k.startswith('title_')}
        self.href = href
        if href is not None:
            self.title_kwargs['href'] = href
        if title is not None:
            self.title_kwargs['title'] = title

        self.ul_element = ul(cls='cs-nav__block-items')
        kwargs = {k: v for k, v in kwargs.items() if not k.startswith('title_')}
        super().__init__(**kwargs)

    def add_link(self, *args, **kwargs):
        """
        Adds a new link to nav section.
        """

        link = hyperlink(*args, **kwargs)
        self.links.append(link)

    def render(self, **kwargs):
        items = [li(x) for x in self.links]
        dom = nav(cls='cs-nav__block')[
            self.title_element,
            ul(items, cls='cs-nav__block-items'),
        ]
        return dom.render(**kwargs)
