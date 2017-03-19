import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render

from .import forms
from . import ctl


def push_question_ctl_view(request):
    """
    Allows a admin user to push a question defined in a external file to the
    server.
    """

    if request.method == 'GET':
        context = {'form': forms.PushQuestionForm()}
    elif request.method == 'POST':
        form = forms.PushQuestionForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            filename = form.cleaned_data['filename']
            contents = form.cleaned_data['contents']
            parent = form.cleaned_data['parent']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            response = ctl.push_question_json(filename, contents, parent, user)

            if form.cleaned_data['response_format'] == 'JSON':
                return JsonResponse(response)
            else:
                context['response'] = json.dumps(response)
    return render(request, 'questions/push_question_ctl.jinja2', context)