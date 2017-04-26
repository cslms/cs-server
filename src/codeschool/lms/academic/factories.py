from codeschool.factories import make_page


def make_cs101_discipline():
    return make_page(
        'academic.Discipline',
        name='Programming 101',
        slug='cs101',
        description=(
            'Introductory programming course. Teachers basic programming '
            'concepts and enable students to make small software projects.'
        ),
        syllabus=(
            '<ul>'
            '<li>Variables and functions</li>'
            '<li>Conditionals and control loops</li>'
            '<li>Data structures</li>'
            '<li>Algorithms</li>'
            '</ul>'
        )
    )
