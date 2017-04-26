from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from codeschool.social.friends import get_all_friends, get_possible_friends, \
    request_friendship
from codeschool.models import User


@login_required
def friends_view(request):
    context = {
        'friends': get_all_friends(request.user),
    }
    if request.method == 'POST':
        print(request.POST)

    return render(request, 'social/friends.jinja2', context)


@login_required
def add_friends_view(request):
    context = {
        'possible_friends': get_possible_friends(request.user),
    }
    if request.method == 'POST':
        items = request.POST.items()
        marked_users = {k[5:] for k, v in items if k.startswith('user-')}
        users = User.objects.filter(username__in=marked_users)
        for user in users:
            request_friendship(request.user, user)
        return redirect('social:friends')
    return render(request, 'social/friends-add.jinja2', context)
