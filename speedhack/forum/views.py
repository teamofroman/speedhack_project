from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from users.models import CustomUser

from .forms import ProfileCommentForm, CommentForm, PostForm
from .models import Follow, Forum, User, ProfileComment


def pagination_post(request, post_list):
	paginator = Paginator(post_list, 12)
	return paginator.get_page(request.GET.get('page'))


def pagination_sub(request, sub_list):
	paginator = Paginator(sub_list, 5)
	return paginator.get_page(request.GET.get('page'))


def pagination_comments(request, comment_list):
	paginator = Paginator(comment_list, 5)
	return paginator.get_page(request.GET.get('page'))


def index(request):
	posts = Forum.objects.select_related('author').all()
	template = 'forum/index.html'
	context = {
		'objects': pagination_post(request, posts)
	}
	return render(request, template, context)


def profile(request, username):
	author = get_object_or_404(User, username=username)
	co = get_object_or_404(ProfileComment, author=author)
	if request.method == 'POST':
		form = ProfileCommentForm(request.POST or None)
	else:
		form = ProfileCommentForm()
	posts = author.posts.all()
	subscriptions = author.follower.all()
	profile_comments = author.co.all()
	subscribers = author.following.all()
	following = (
		author.following.filter(user_id=request.user.id).exists()
		if request.user.is_authenticated
		else False
	)
	count_posts = posts.count()
	count_profile_comments = profile_comments.count()
	count_subscriptions = subscriptions.count()
	count_subscribers = subscribers.count()
	template = 'forum/profile.html'
	context = {
		'author': author,
		'form': form,
		'following': following,
		'count_posts': count_posts,
		'count_profile_comments': count_profile_comments,
		'count_subscriptions': count_subscriptions,
		'count_subscribers': count_subscribers,
		'objects': pagination_post(request, posts),
		'subscriptions': pagination_sub(request, subscriptions),
		'subscribers': pagination_sub(request, subscribers),
		'profile_comments': pagination_comments(request, profile_comments),
	}
	return render(request, template, context)


@login_required
def add_comment_profile(request, username):
	form = ProfileCommentForm(request.POST or None)
	if form.is_valid():
		comment = form.save(commit=False)
		comment.author = request.user
		comment.save()
	return redirect('forum:profile', username=username)


def post_detail(request, post_id):
	post = get_object_or_404(Forum, id=post_id)
	form = CommentForm(request.POST or None)
	comments = post.comments.all()
	template = 'forum/post_detail.html'
	context = {
		'form': form,
		'post': post,
		'comments': comments
	}
	return render(request, template, context)


@login_required
def post_create(request):
	form = PostForm(
		request.POST or None,
		files=request.FILES or None
	)
	if request.method == 'POST':
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()
			return redirect('forum:index')
	template = 'forum/post_create.html'
	context = {
		'form': form
	}
	return render(request, template, context)


@login_required
def add_comment(request, post_id):
	post = get_object_or_404(Forum, pk=post_id)
	form = CommentForm(request.POST or None)
	if form.is_valid():
		comment = form.save(commit=False)
		comment.author = request.user
		comment.post = post
		comment.save()
	return redirect('forum:post_detail', post_id=post_id)


@login_required
def profile_follow(request, username):
	author = get_object_or_404(User, username=username)
	if author != request.user:
		if not Follow.objects.filter(author=author, user=request.user).exists():
			Follow.objects.create(author=author, user=request.user)
	return redirect('forum:profile', username=username)


@login_required
def profile_unfollow(request, username):
	author = get_object_or_404(User, username=username)
	author.following.filter(user=request.user).delete()
	return redirect('forum:profile', username=username)


@login_required
def admin_panel(request):
	template = 'forum/admin.html'
	author = Forum.objects.select_related('author').all()
	users_list = CustomUser.objects.all()
	context = {
		'author': author,
		'users': users_list,
	}
	return render(request, template, context)


def faq(request):
	template = 'forum/faq.html'
	return render(request, template)


def politic(request):
	template = 'forum/politic.html'
	return render(request, template)


def rules(request):
	template = 'forum/rules.html'
	return render(request, template)


def users(request):
	template = 'forum/users.html'
	author = Forum.objects.select_related('author').all()
	users_list = CustomUser.objects.all()
	context = {
		'author': author,
		'users': users_list,
	}
	return render(request, template, context)
