import model_reference


def course_list(request):
    page = model_reference.load('course-list')
    return page.serve(request)
