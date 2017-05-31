from codeschool.bricks import navbar as _navbar, navsection, navsection_page_admin
from bricks.html5 import a
from codeschool.bricks import card_container, simple_card

def navbar():
    return _navbar([
        navsection('Menu',
            [a('Home Sparta', href='#'),
            a('Mensagens', href='#')
        ])])

def layout():
    cards = [
        simple_card('card1','bla bla bla', double=True, center=False),
        simple_card('Atividades','Atividades a fazer', icon='assignment'),
        simple_card('Notas','Atividades avaliadas', icon='star', href='#'),        
    ]

    return card_container(cards, title='Membros', description='Lista dos membros')
