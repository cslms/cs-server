from django.template.loader import render_to_string


def render_dialog(attendance_sheet, request):
    """
    Renders attendance dialog based on request.
    """

    context = {
        'passphrase': attendance_sheet.passphrase,
        'is_expired': attendance_sheet.is_expired(),
        'minutes_left': attendance_sheet.minutes_left(raises=False)
    }
    user = request.user
    if user == attendance_sheet.owner:
        template = 'attendance/edit.jinja2'
    else:
        template = 'attendance/view.jinja2'
        context['attempts'] = attendance_sheet.user_attempts(user)
    return render_to_string(template, request=request, context=context)
