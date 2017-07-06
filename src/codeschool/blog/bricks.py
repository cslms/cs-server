from codeschool.bricks import navbar as _navbar, navsection, navsection_page_admin
from bricks.html5 import a, div, h1, h2, ul, li, button
from codeschool.bricks import card_container, simple_card, with_class
from simple_search import search_filter
from .models import Post, Comment
from codeschool.models import User

# import members_list from back end

def navbar():
    return _navbar([
        navsection('Menu',
            [a('Home Blog', href='#'),
            a('Mensagens', href='#')
        ])])

@with_class('cs-sparta')
def layout():
    cards = [
        simple_card('card1','bla bla bla', double=True, center=False),
        simple_card('Atividades','Atividades a fazer', icon='assignment', href='/sparta/activities'),
        simple_card('Notas','Atividades avaliadas', icon='star', href='#'),
    ]

    # TODO: Import from backend
    from types import SimpleNamespace
    Member = SimpleNamespace
    all_users = Post.objects.all()


    b = div()[
        ul(class_="cs-sparta__members-list",)[[
            li(a(post.title, href='#')) for post in all_users
        ]],
        button(class_="button")(
                'Avaliar membros', href='#')
    ]
    return card_container(cards, title='Membros', description=b)

def activities_layout():

    # TODO: Import from backend
    from types import SimpleNamespace
    Activity = SimpleNamespace
    activities_list = [Activity(name="Atividade 1"), Activity(name="Atividade 2"), Activity(name="Atividade 3", url="dfsdf")]

    # activities_list = activity_filter()

    cards = [ simple_card(activity.name, double=True, center=False) for activity in activities_list ]
    return card_container(cards)