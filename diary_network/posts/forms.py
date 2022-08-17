from django.forms import ModelForm, Textarea

from .models import Comment, Group, Post, User


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


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Комментарий'
        }
        widgets = {
            'text': Textarea(attrs={'rows': 3}),
        }


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя*',
            'email': 'Адрес электронной почты'
        }
