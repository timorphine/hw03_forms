from django.shortcuts import get_object_or_404, render
from .models import Group, Post, User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import PostForm
from django.shortcuts import redirect


def index(request):
    posts = Post.objects.all()
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page_number)
    context = {
        "posts": posts,
        "page_obj": page_obj
    }
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.all().filter(group=group)
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page_number)
    context = {
        "group": group,
        "page_obj": page_obj,
    }
    return render(request, "posts/group_list.html", context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.all().filter(author=author)
    page_number = request.GET.get('page')
    paginator = Paginator(post_list, 10)
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "post_list": post_list,
        "author": author,
    }
    return render(request, "posts/profile.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_list = Post.objects.all().filter(author_id=post.author)
    context = {
        "post": post,
        "post_list": post_list
    }
    return render(request, "posts/post_detail.html", context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.id and request.user != post.author:
        redirect('posts:profile', request.user)
    is_edit = True
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post_id)
    context = {
        "form": form,
        "post": post,
        "is_edit": is_edit
    }
    return render(request, 'posts/create_post.html', context)
