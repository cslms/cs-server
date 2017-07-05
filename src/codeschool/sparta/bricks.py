from codeschool.bricks import navbar as _navbar, navsection, navsection_page_admin
from bricks.html5 import ul, li, a, i, select, option, input, table, tbody, thead, th, td, tr, div, h2, button, div, form, button
from codeschool.bricks import card_container, simple_card, with_class
from django.urls import reverse
from .models.activity import UserRating
# import members_list from back end


def navbar():
    return _navbar([
        navsection('Menu',
                   [a('Home Sparta', href='#'),
                    a('Mensagens', href='#')
                    ])])


@with_class('cs-sparta')
def layout():
    cards = [
        simple_card('card1', 'bla bla bla', double=True, center=False),
        simple_card('Atividades', 'Atividades a fazer',
                    icon='assignment', href='/sparta/activities'),
        simple_card('Notas', 'Atividades avaliadas', icon='star', href='#'),
    ]

    # TODO: Import from backend
    from types import SimpleNamespace
    Member = SimpleNamespace
    members_list = [Member(name="Goku"), Member(
        name="Ronaldo"), Member(name="Florentina", url="dfsdf")]

    b = div()[
        ul(class_="cs-sparta__members-list",)[[
            li(a(member.name, href='#')) for member in members_list
        ]],
        a(class_="button", href=reverse('sparta_rating'))[
            ('Avaliar')
        ]
    ]
    return card_container(cards, title='Membros', description=b)


def activities_layout():

    # TODO: Import from backend
    from types import SimpleNamespace
    Activity = SimpleNamespace
    activities_list = [Activity(name="Atividade 1"), Activity(
        name="Atividade 2"), Activity(name="Atividade 3", url="dfsdf")]

    # activities_list = activity_filter()

    cards = [simple_card(activity.name, double=True, center=False)
             for activity in activities_list]
    return card_container(cards)


def rating_layout(members):
    user_rows = []
    for user in members:
        try:
            evaluations = UserRating.objects.filter(user_evaluated=user)
        except:
            evaluations = []

        average = 0.0
        for evaluation in evaluations:
            average += evaluation.rating

        if average > 0:
            average /= len(evaluations)
        
        user_rows.append(
            form(action='')[
                tr()[
                    td(class_="mdl-data-table__cell--non-numeric")[
                        user.first_name + ' ' + user.last_name],
                    td()[str(len(evaluations)) + ' Aluno(s)'],
                    td()[str(average)],
                    td()[
                        div(class_="cs-sparta__rateYo"),
                        button(type="submit")['Submit']
                    ],
                ]
            ]
        )

    layout = ul(class_="demo-list-icon mdl-list")[
        table(class_="mdl-data-table mdl-js-data-table mdl-shadow--2dp")[
            div(class_="mdl-tooltip", for_="tt1")['Já Avaliado'],
            thead()[
                tr()[
                    th(class_="mdl-data-table__cell--non-numeric")['Aluno'],
                    th()['Avaliações'],
                    th()['Nota'],
                    th()['Avaliar'],
                ]
            ],
            tbody()[
                user_rows
            ],
        ],
    ]
    return layout
