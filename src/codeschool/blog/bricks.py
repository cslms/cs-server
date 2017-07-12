from codeschool.bricks import navbar as _navbar, navsection, navsection_page_admin
from bricks.html5 import a,p, div, h1, h2, ul, li, button, br
from codeschool.bricks import card_container, simple_card, with_class
from simple_search import search_filter

#Posts
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm

def posts_layout(posts, users):
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
            li(a(user.username, href='/blog/user/{}'.format(user.id),)) for user in users
        ]],
    ]
    return card_container(cards, title='Membros', description=b)

def navbar(user_id, users):

    return _navbar([
        navsection('Menu',
            [
                a('New Post', href='/blog/post/new'),
                a('Posts', href='/blog'),
                a('Minhas postagens', href='/blog/user/{}/'.format(user_id))
            ]
        ),
        br,
        navsection('Membros',
            [
               a(user.username, href='/blog/user/{}'.format(user.id),) for user in users
            ]
        ),
    ])