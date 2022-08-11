from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def page_not_found(request, exception):
    return render(
        request, 
        "misc/404.html", 
        {"path": request.path}, 
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


@login_required
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")
    return render(request, "group.html", {"group": group, "posts": posts})


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')

        return render(request, 'post_new.html', {'form': form})

    form = PostForm()
    return render(request, 'post_new.html', {'form': form})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author = profile).order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    posts_count = post_list.count()
    page = paginator.get_page(page_number)
    context = {"profile": profile, "page": page, "paginator": paginator, "posts_count": posts_count}
    return render(request, "profile.html", context)
 
 
def post_view(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    post_list = Post.objects.filter(author = profile).order_by("-pub_date").all()
    posts_count = post_list.count()
    context = {
        "profile": profile, 
        "post": post,
        "posts_count": posts_count, 
    } 
    return render(request, 'post.html', context)


def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect("post", username=user.username, post_id=post_id)

    title = "Редактировать запись"
    btn_caption = "Сохранить"
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post", username=request.user.username, post_id=post_id)
    return render(request, "post_new.html", {"form": form, "title": title, "btn_caption": btn_caption, "post": post})
