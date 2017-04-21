import model_reference


def make_basic_activities():
    page = model_reference.load('main-question-list')
    page.update_from_template('programming-beginner')
    return page
