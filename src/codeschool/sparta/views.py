from django.shortcuts import render
from bricks.contrib.mdl import button, div
from bricks.html5 import ul, li, a, i, select, option, input, table, tbody, thead, th, td, tr
from codeschool.bricks import navbar as _navbar, navsection
from .bricks import navbar, layout, activities_layout

# Create your views here.
def index(request):

    ctx = {
    'main':layout(),
    'navbar':navbar(),
    }
    return render(request, 'sparta/index.jinja2', ctx)

def activities(request):

    ctx = {
    'content_title':'Atividades',
    'content_body':activities_layout(),
    }
    return render(request, 'sparta/activities.jinja2', ctx)

def rating(request):

    ctx = {
        'content_title':'Avaliação dos Membros',
        'content_body': ul(class_="demo-list-icon mdl-list")[
        table(class_="mdl-data-table mdl-js-data-table mdl-shadow--2dp")[
          thead()[
            tr()[
              th(class_="mdl-data-table__cell--non-numeric")['Aluno'],
              th()['Avaliações'],
              th()['Nota'],
              th()['Avaliado?'],
            ]
          ],
          tbody()[
            tr()[
              td(class_="mdl-data-table__cell--non-numeric")['Goku da Silva Mendes'],
              td()['3 Aluno(s)'],
              td()['10'],
              td()[
                i(class_="material-icons")['done'],
                ]
            ],
            tr()[
              td(class_="mdl-data-table__cell--non-numeric")['Ronaldo Andrade Souza'],
              td()['0 Aluno(s)'],
              td()['0'],
              td()['-'],
            ],
            tr()[
              td(class_="mdl-data-table__cell--non-numeric")['Florentina de Jesus'],
              td()['0 Aluno(s)'],
              td()['0'],
              td()['-'],
            ],

          ]
        ],
    ]
    }
    return render(request, 'sparta/rating.jinja2', ctx)
