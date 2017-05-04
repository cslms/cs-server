from django.utils.translation import ugettext_lazy as _

from bricks.components.utils import ifset
from bricks.helpers import js_class, join_classes
from bricks.html5 import div, a_or_span, h1, p, aside, article, section
from . import mdl


def simple_card(title=None, text=None, href=None, icon='help', faded=False,
                onclick=None, id=None, class_=None, empty=False):
    """
    Returns HTML for a cs-card block.

    This function accepts multiple dispatch and clients might register
    different implementations for specific models/types.

    Args:
        title:
            Card title.
        text:
            Card description and main content.
        href:
            Optional address for the class icon.
        icon:
            Material icon for card.
        faded:
            If True, card is rendered with the faded state.
        onclick:
            Action to be associated with the onclick event.
        id/class_:
            Card's id/class attributes.
    """
    # Defaults for empty cards
    if empty:
        faded = True
        title = title or _('Empty')
        text = text or _('Not found'),
        icon = icon or 'do_not_disturb',

    class_ = js_class('cs-card mdl-shadow--4dp', 'mdl-cell',
                      faded and 'cs-card--faded',
                      class_)
    icon = mdl.icon(class_='cs-card__icon')[icon]
    icon = a_or_span(href=href, onclick=onclick, class_='cs-card__link')[icon]

    return \
        div(class_=class_, id=id)[
            icon,
            title and h1(class_='cs-card__title')[title],
            text and p(text)
        ]


def card_container(cards, title=None, description=None, class_=None,
                   empty=None, **kwargs):
    """
    A container for simple card elements.

    Args:
        cards:
            A list of cards.
        title:
            Title to show to the LHS of the container.
        description:
            Short description bellow title.
    """
    lhs_aside = None
    if title:
        cls = 'cs-card-container__aside mdl-cell mdl-cell--3-col'
        lhs_aside = \
            aside(class_=cls)[
                h1(title),
                description and p(description)
            ]

    ncols = 9 if title else 12
    cls = join_classes('cs-card-container mdl-grid mdl-grid--no-spacing',
                       class_)
    return \
        div(class_='bg-primary layout-wfull')[
            section(class_=cls)[
                ifset(title, lhs_aside),

                article(class_='mdl-cell mdl-cell--%s-col' % ncols)[
                    div(class_='cs-card-aside__content mdl-grid')[
                        cards or [empty],
                    ]
                ],
            ]
        ]
