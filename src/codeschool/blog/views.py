from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#bricks modules
from bricks.contrib.mdl import button, div
from bricks.html5 import ul, li, a, i, select, option, input, table, tbody, thead, th, td, tr
from codeschool.bricks import navbar as _navbar, navsection
from .bricks import navbar, posts_layout, detail_layout, navbar_configuration

# Create your views here.
def index(request):
    posts = (
        Post.objects
            .filter(created_date__lte=timezone.now())
            .order_by('-created_date')
            .select_related('author')
    )
    users = User.objects.filter(id__in={post.author_id for post in posts }) 


    ctx = {'posts' : posts, 'users':users}
    return render(request, 'blog/index.j2', ctx)

def post_list(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    ctx = {'posts' : posts}
    return render(request, 'blog/post_list.j2', ctx)

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    user_id = post.author_id

    form = CommentForm()

    if request.user.id == user_id:
        ctx = {
            'navbar':navbar_configuration(user_id=user_id),
            'post': post,
            'comments': comments,
            'form': form,
        }
    else:
        ctx = {
            'navbar':navbar(user_id=user_id),
            'post': post,
            'comments': comments,
            'form': form,
        }
    return render(request, 'blog/post_detail.j2', ctx)

@login_required
def user_posts(request, pk):
    user = get_object_or_404(User, pk=pk)
    posts_of_user = (
        Post.objects
            .filter(author__username=user.username)
            .order_by('-created_date')
            .select_related('author')
    )

    all_posts = (
    Post.objects
        .filter(created_date__lte=timezone.now())
        .order_by('-created_date')
        .select_related('author')
    )
    users = User.objects.filter(id__in={post.author_id for post in all_posts }) 
    ctx = {
        'users': users,
        'posts': posts_of_user,
    }
    return render(request, 'blog/user_posts.j2', ctx)
    
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=post)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog:postdetail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.j2', {'form': form})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish()
            return redirect('blog:postdetail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.j2', { 'form': form, 'type': "New Post" })

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_id = request.user.id
    if request.user.id == post.author_id:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('blog:postdetail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.j2', {'form': form, 'type': "Edit Post", 'navbar': navbar(user_id=user_id)})
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.j2', { 'form': form, 'type': "Edit Post" })

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.id == post.author_id:
        post.delete()
    return redirect('blog:postlist')

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:postdetail', pk=post_pk)