from codeschool.bricks import navbar as _navbar, navsection, navsection_page_admin
from bricks.html5 import a, div, h1, h2, ul, li, button
from codeschool.bricks import card_container, simple_card, with_class
from simple_search import search_filter
<<<<<<< HEAD
from .models import Post, Comment
from codeschool.models import User

# import members_list from back end
=======

#Posts
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
>>>>>>> colocando posts do usuário

def navbar():
    return _navbar([
        navsection('Menu',
<<<<<<< HEAD
            [a('Home Blog', href='#'),
            a('Mensagens', href='#')
=======
            [a('Posts', href='#'),
            a('Minhas postagens', href='#')
>>>>>>> colocando posts do usuário
        ])])

def layout():
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    cards = [
        simple_card(
            post.text, 
            'Author: {}'.format(post.author.username), 
            href='post/{}'.format(post.id),
            icon='forum', 
            double=True, 
            center=False
        ) 
        for post in posts 
    ]

    # TODO: Kassia
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

def detail_layout(post):
    card = simple_card(
        post.text, 
        'Author: {}'.format(post.author.username), 
        icon='forum', 
        double=True, 
        center=False
    ) 
    return card

def posts_layout():

    # TODO: Import from backend
    from types import SimpleNamespace
    Activity = SimpleNamespace
    activities_list = [Activity(name="Atividade 1"), Activity(name="Atividade 2"), Activity(name="Atividade 3", url="dfsdf")]

    # activities_list = activity_filter()

    cards = [ simple_card(activity.name, double=True, center=False) for activity in activities_list ]
    return card_container(cards)

def comments_layout():

    # TODO: Import from backend
    from types import SimpleNamespace
    Activity = SimpleNamespace
    activities_list = [Activity(name="Atividade 1"), Activity(name="Atividade 2"), Activity(name="Atividade 3", url="dfsdf")]

    # activities_list = activity_filter()

    cards = [ simple_card(activity.name, double=True, center=False) for activity in activities_list ]
    return card_container(cards)