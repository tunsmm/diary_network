from django.forms import ModelForm

from .models import Group, Post


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'slug', 'description']
        labels = {
            'title': ('Название'),
            'slug': ('Уникальный URL'),
            'description': ('Описание группы'),
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']
        labels = {
            'group': ('Группа'),
            'text': ('Текст'),
        }
