import itertools

from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from codeschool.social.feed import get_user_feeds
from codeschool.social.feed.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['text', 'visibility']


@login_required
def timeline_view(request):
    feeds = list(itertools.islice(get_user_feeds(request.user), 20))
    context = {
        'feeds': feeds,
    }
    return render(request, 'social/timeline.jinja2', context)


@login_required
def feed_view(request):
    context = {
        'posts': Post.objects.filter(user=request.user).order_by('-created'),
        'post_id': request.GET.get('post-id')
    }
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('./?post-id:%s' % post.id)
    else:
        form = PostForm()
    context['form'] = form
    return render(request, 'social/feed.jinja2', context)
