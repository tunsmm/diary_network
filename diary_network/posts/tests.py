from django.test import TestCase, Client
from .models import Post, User


class PostsCasesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="TestUser", email="mail@mail.ru", password="asdfgh12ter")
        self.client.login(username="TestUser", password="asdfgh12ter")
    
    def test_user_post(self):
        """Авторизованный пользователь может опубликовать пост (new)"""
        self.post = Post.objects.create(text="Test post", author=self.user)
        response = self.client.get("/TestUser/")
        self.assertEqual(response.context["posts_count"], 1)

    def test_logout_post(self):
        """Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)"""
        self.client.logout()
        response = self.client.get("/new/", follow=True)
        self.assertEqual([("/accounts/login/?next=/new/", 302)], response.redirect_chain)


class NewPostCaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="TestUser", email="mail@mail.ru", password="asdfgh12ter")
        self.client.login(username="TestUser", password="asdfgh12ter")
        self.post = Post.objects.create(text=("Test post"), author=self.user)

    def test_new_post_index(self):
        """После публикации поста новая запись появляется на главной странице сайта (index)"""
        response = self.client.get("")
        self.assertContains(response, self.post.text)
    
    def test_new_post_profile(self):
        """После публикации поста новая запись появляется на персональной странице пользователя (profile)"""
        response = self.client.get(f"/{self.user.username}/")
        self.assertContains(response, self.post.text)

    def test_new_post_view(self):
        """После публикации поста новая запись появляется на отдельной странице поста (post)"""
        response = self.client.get(f"/{self.user.username}/{self.post.pk}/")
        self.assertContains(response, self.post.text)


class PostEditCaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
                        username="TestUser", email="mail@mail.ru", password="asdfgh12ter"
                )
        self.client.login(username="TestUser", password="asdfgh12ter")
        self.post = Post.objects.create(text=("Test post"), author=self.user)
        self.new_text = "New Test"
        self.client.post(f"/{self.user.username}/{self.post.pk}/edit/", {"text": self.new_text})

    def test_postedit_index(self):
        """Авторизованный пользователь может отредактировать свой пост
         и его содержимое изменится на главной странице сайта (index)"""
        response = self.client.get("")
        self.assertContains(response, self.new_text)

    def test_postedit_profile(self):
        """Авторизованный пользователь может отредактировать свой пост
         и его содержимое изменится на персональной странице пользователя (profile)"""
        response = self.client.get(f"/{self.user.username}/")
        self.assertContains(response, self.new_text)
    
    def test_postedit_view(self):
        """Авторизованный пользователь может отредактировать свой пост
         и его содержимое изменится на отдельной странице поста (post)"""
        response = self.client.get(f"/{self.user.username}/{self.post.pk}/")
        self.assertContains(response, self.new_text)
