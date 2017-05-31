from codeschool.bricks import navbar as _navbar, navsection, navsection_page_admin
from bricks.html5 import a
from codeschool.bricks import card_container, simple_card

def navbar():
    return _navbar([
        navsection('Titulo',
            [a('Bla bla', href='#'),
            a('bla bla2', href='#')
        ])])

def layout():
    cards = [
        simple_card('card1','bla bla bla', double=True, center=False),
        simple_card('card2','bla bla bla', icon='code'),
        simple_card('card3','bla bla bla', icon='play', href='#'),        
    ]

    return card_container(cards, title='Cards description', description='uma descrição')
