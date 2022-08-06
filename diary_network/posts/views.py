from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Group, Post


"""
Post.objects.all() — получить все записи модели Post
Post.objects.get(id=1) — получить запись модели Post, у которой значение поля id равно 1. Поскольку поле id — это первичный ключ, а Django автоматически создаёт у модели свойство pk, то альтернативная запись этого же запроса будет такой: Post.objects.get(pk=1).
Post.objects.filter(pub_date__year=1854) — запрос вернёт объекты, у которых значение года в поле pub_date равно 1854. Обратите внимание на синтаксис фильтрации: двойное нижнее подчёркивание между названиями поля и фильтра. Подробнее о функции filter() — в документации.
Post.objects.filter(text__startswith="Писать не хочется") — пример фильтра по текстовому полю, он вернёт записи, начинающиеся с указанной в фильтре строки.
"""


@login_required
def index(request):
    latest = Post.objects.order_by("-pub_date")[:11]
    return render(request, "index.html", {"posts": latest})


@login_required
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")
    return render(request, "group.html", {"group": group, "posts": posts})
