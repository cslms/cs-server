from codeschool.bricks import navbar as _navbar, navsection, navsection_page_admin
from bricks.html5 import a,p, div, h1, h2, ul, li, button
from codeschool.bricks import card_container, simple_card, with_class
from simple_search import search_filter

#Posts
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

def navbar():
    return _navbar([
        navsection('Menu',
            [a('Posts', href='#'),
            a('Minhas postagens', href='#')
        ])])

def layout(posts, users):
    cards = [
        simple_card(
            post.title, 
            'Author: {}'.format(post.author.username), 
            href='post/{}'.format(post.id),
            icon='forum', 
            double=True, 
            center=False
        ) 
        for post in posts 
    ]

    b = div()[
        ul(class_="cs-sparta__members-list",)[[
            li(a(user.username, href='user/{}'.format(user.id),)) for user in users
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

    card2 = [
        p("Comentários: {}".format(post.comments.count()))

    ]

    cards = [
        simple_card(
            comment.text, 
            'Author: {}'.format(comment.author.username), 
            icon='comment', 
            double=True, 
            center=False
        ) 
        for comment in post.comments.all()
    ]
    cards.insert(0,card)
    cards.insert(1,card2)

    return card_container(cards, title=post.title)


def my_posts(posts):

    cards = [
        simple_card(
            post.text, 
            icon='forum', 
            double=True, 
            center=False
        ) 
        for post in posts
    ]

    return card_container(cards, title=post.title)

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