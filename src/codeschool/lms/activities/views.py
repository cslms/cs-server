import model_reference


def main_question_list(request):
    page = model_reference.load('main-question-list')
    return page.serve(request)