from codeschool.bricks import navbar as _navbar, navsection, navsection_page_admin
from bricks.html5 import a, div, h1, h2, ul, li, button
from codeschool.bricks import card_container, simple_card, with_class

def navbar():
    return _navbar([
        navsection('Menu',
            [a('Home Sparta', href='#'),
            a('Mensagens', href='#')
        ])])

@with_class('cs-sparta')
def layout():
    cards = [
        simple_card('card1','bla bla bla', double=True, center=False),
        simple_card('Atividades','Atividades a fazer', icon='assignment', href='/sparta/activities'),
        simple_card('Notas','Atividades avaliadas', icon='star', href='#'),        
    ]

    b = div()[
        ul(class_="cs-sparta__members-list",)[
            li(a('Josefina', href='#')),
            li(a('Xablau', href='#')),
            li(a('Xitãozinho', href='#')),
        ],
        button(class_="button")(
                'Avaliar membros', href='#')
    ]
    return card_container(cards, title='Membros', description=b)
