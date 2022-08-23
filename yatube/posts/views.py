from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .utils import custom_paginator
from .forms import PostForm
from .models import Group, Post, User


POSTS_PER_PAGE = 10


def index(request):
    post_list = Post.objects.all()
    page_obj = custom_paginator(request, post_list, POSTS_PER_PAGE)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = custom_paginator(request, posts, POSTS_PER_PAGE)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    count_post = post_list.count()
    page_obj = custom_paginator(request, post_list, POSTS_PER_PAGE)

    context = {
        'author': author,
        'page_obj': page_obj,
        'count': count_post,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post_detail = get_object_or_404(Post, pk=post_id)
    author = post_detail.author
    count = author.posts.count()
    context = {
        'author': author,
        'post_detail': post_detail,
        'count': count,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            auth_user = request.user
            new_post = form.save(commit=False)
            new_post.author = auth_user
            new_post.save()
            return redirect('posts:profile', username=auth_user)

        return render(request, template, {'form': form})

    else:
        form = PostForm()

    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, id=post_id)

    context = {
        'is_edit': True,
    }

    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = post.author
            new_post.save()
            return redirect('posts:post_detail', post_id=post_id)

        return render(request, template, context)

    else:
        form = PostForm(instance=post)

    context['form'] = form
    return render(request, template, context)
