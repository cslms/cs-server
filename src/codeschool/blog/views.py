from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

#bricks modules
from bricks.contrib.mdl import button, div
from bricks.html5 import ul, li, a, i, select, option, input, table, tbody, thead, th, td, tr
from codeschool.bricks import navbar as _navbar, navsection
from .bricks import navbar, layout, posts_layout, comments_layout, detail_layout

# Create your views here.
def index(request):

    ctx = {
    'main':layout(),
    'navbar':navbar(),
    }
    return render(request, 'blog/index.jinja2', ctx)

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    ctx = {
        'main':detail_layout(post),
        'navbar':navbar(),
    }
    return render(request, 'blog/post_detail.jinja2', ctx)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog:postdetail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.jinja2', {'form': form})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    ctx = {'posts' : posts}
    return render(request, 'blog/post_list.jinja2', ctx)

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:postdetail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.jinja2', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:postdetail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.jinja2', {'form': form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:postlist')

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:postlist')

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:postdetail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:postdetail', pk=post_pk)
