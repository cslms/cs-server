from codeschool.bricks import navbar as _navbar, navsection, navsection_page_admin
from bricks.html5 import p, ul, li, a, i, select, option, input, table, tbody, thead, th, td, tr, div, h2, button, div, form, button
from codeschool.bricks import card_container, simple_card, with_class
from django.urls import reverse
from .models.activity import UserRating
from .models import SpartaMembership, SpartaGroup
# import members_list from back end


def navbar():
    return _navbar([
        navsection('Menu',
                   [a('Home Sparta', href='#'),
                    a('Mensagens', href='#')
                    ])])


@with_class('cs-sparta')
def layout(current_user):
    cards = [
        simple_card('card1', 'bla bla bla', double=True, center=False),
        simple_card('Atividades', 'Atividades a fazer',
                    icon='assignment', href='/sparta/activities'),
        simple_card('Notas', 'Atividades avaliadas', icon='star', href='#'),
    ]

    # TODO: Import from backend
    from types import SimpleNamespace
    Member = SimpleNamespace
    members = __members_group(current_user)
    members_list = []
    for member in members:
        members_list.append(Member(name=member.first_name + ' ' + member.last_name))

    user_evaluations = __user_evaluations(current_user)
    user_rating = 0
    for evaluation in user_evaluations:
        user_rating += evaluation.rating
    if user_rating != 0:
        user_rating /= len(user_evaluations)

    b = div()[
        ul(class_="cs-sparta__members-list",)[[
            li(a(member.name, href='#')) for member in members_list
        ]],
        div(class_="cs-sparta__button-container")[
            a(class_="button", href=reverse('sparta_rating'))[
                ('Avaliar')
            ]
        ],
        div(class_="cs-sparta__your-rating",)[
                ('Sua média de avaliação é '),
                p(str(user_rating))
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


def rating_layout(user_evaluatee):
    user_rows = []
    members = __members_group(user_evaluatee)
    for user_evaluated in members:
        evaluations =  __user_evaluations(user_evaluated)
        evaluation = __user_evaluation(user_evaluated, user_evaluatee)      

        if user_evaluated != user_evaluatee:
            user_rows.append(
                tr()[
                    td(class_="mdl-data-table__cell--non-numeric")[
                        user_evaluated.first_name + ' ' + user_evaluated.last_name],
                    td(id="RLen-"+str(user_evaluated.id))[str(len(evaluations)) + ' Aluno(s)'],
                    td()[
                        div(class_="cs-sparta__rateYo", 
                            id='RUser-'+str(user_evaluated.id)+'-'+str(evaluation))
                    ],
                ]
            )

    layout = ul(class_="demo-list-icon mdl-list")[
        table(class_="mdl-data-table mdl-js-data-table mdl-shadow--2dp")[
            div(class_="mdl-tooltip", for_="tt1")['Já Avaliado'],
            thead()[
                tr()[
                    th(class_="mdl-data-table__cell--non-numeric")['Aluno'],
                    th()['Avaliações'],
                    th()['Avaliar'],
                ]
            ],
            tbody()[
                user_rows
            ],
        ],
    ]
    return layout

def __members_group(user):
    membership = SpartaMembership.objects.get(user=user)
    group = membership.group
    return group.members.all()

def __user_evaluations(user):
    try:
        evaluations =  UserRating.objects.filter(user_evaluated=user)
            
    except:
        evaluations = []

    return evaluations

def __user_evaluation(user_evaluated, user_evaluatee):
    try:
        evaluation =  UserRating.objects.get(user_evaluated=user_evaluated,
                                user_evaluatee=user_evaluatee).rating
    except:
        evaluation = 0
    
    return evaluation