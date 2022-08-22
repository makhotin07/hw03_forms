from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import PostForm
from .models import Group
from .models import Post
from .models import User

POSTS_PER_PAGE = 10


def index(request):
	post_list = Post.objects.all().order_by('-pub_date')
	paginator = Paginator(post_list, POSTS_PER_PAGE)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		'page_obj': page_obj,
	}
	return render(request, 'posts/index.html', context)


def group_posts(request, slug):
	template = 'posts/group_list.html'
	group = get_object_or_404(Group, slug = slug)
	posts = Post.objects.filter(group = group).order_by('-pub_date')
	paginator = Paginator(posts, POSTS_PER_PAGE)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'group': group,
		'page_obj': page_obj
	}
	return render(request, template, context)


def profile(request, username):
	template = 'posts/profile.html'
	author = get_object_or_404(User, username = username)
	post_list = Post.objects.filter(author__username = username)
	count = Post.objects.filter(author = author).count()
	paginator = Paginator(post_list, POSTS_PER_PAGE)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		'author': author,
		'page_obj': page_obj,
		'count': count,
	}
	return render(request, template, context)


def post_detail(request, post_id):
	template = 'posts/post_detail.html'
	post_detail = get_object_or_404(Post, pk = post_id)
	author = post_detail.author
	count = Post.objects.filter(author = author).count()
	context = {
		'author': author,
		'post_detail': post_detail,
		'count': count,
	}
	return render(request, template, context)


def post_create(request):
	template = 'posts/create_post.html'

	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			auth_user = request.user
			new_post = form.save(commit = False)
			new_post.author = auth_user
			new_post.save()
			return redirect(f'/profile/{auth_user}/')

		return render(request, template, {'form': form})

	else:
		form = PostForm()

	return render(request, template, {'form': form})


def post_edit(request, post_id):
	template = 'posts/create_post.html'
	post = get_object_or_404(Post, id = post_id)

	context = {
		'is_edit': True,
	}

	if request.user != post.author:
		return redirect('posts:post_detail', post_id = post_id)

	if request.method == 'POST':
		form = PostForm(request.POST)
		context['form'] = form
		if form.is_valid():
			auth_user = request.user
			new_post = form.save(commit = False)
			new_post.author = auth_user
			new_post.save()
			return redirect(f'/posts/{post_id}/')

		return render(request, template, context)

	else:
		form = PostForm(instance = post)
		context['form'] = form

	return render(request, template, context)
