from django.test import TestCase, Client

from .models import Group, Post, User


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
        self.user = User.objects.create_user(username="TestUser", email="mail@mail.ru", password="asdfgh12ter")
        self.client.login(username="TestUser", password="asdfgh12ter")
        self.post = Post.objects.create(text=("Old Test"), author=self.user)
        self.new_text = "New Test"
        self.client.post(f"/{self.user.username}/{self.post.pk}/edit/", {"text": self.new_text})
        
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


class CommentCaseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="TestUser", email="mail@mail.ru", password="asdfgh12ter")
        self.client.login(username="TestUser", password="asdfgh12ter")
        self.post = Post.objects.create(text="Test post", author=self.user)

    def test_comment_authorized(self):
        """Авторизированный пользователь может комментировать посты."""
        self.client.post ("/TestUser/1/comment/", {"text": "Test comment"})
        response = self.client.get("/TestUser/1/")
        self.assertContains(response, "Test comment")

    def test_comment_notauthorized(self):
        """Не авторизированный пользователь не может комментировать посты."""
        self.client.logout()
        self.client.post ("/TestUser/1/comment/", {"text": "Test comment"})
        response = self.client.get("/TestUser/1/")
        self.assertNotContains(response, "Test comment")


class followCaseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
                        username="TestUser", email="mail@mail.ru", password="text2super3"
                )
        self.user2 = User.objects.create_user(
                        username="TestUser2", email="mail2@mail.ru", password="text2super3"
                )
        self.user3 = User.objects.create_user(
                        username="TestUser3", email="mail3@mail.ru", password="text2super3"
                )
        self.client.login(username="TestUser", password="text2super3")
        self.post = Post.objects.create(text="Test post", author=self.user3)

    def test_follow(self):
        """Авторизованный пользователь может подписываться на других пользователей"""
        self.client.get("/TestUser2/follow/")
        response = self.client.get("/TestUser/")
        self.assertEqual(response.context["follows"], 1)

    def test_unfollow(self):
        """Авторизованный пользователь может удалять других пользователей из подписок."""
        self.client.get("/TestUser2/unfollow/")
        response = self.client.get("/TestUser/")
        self.assertEqual(response.context["follows"], 0)
    

    def test_news_lent(self):
        """Новая запись пользователя появляется в ленте тех, кто на него подписан"""
        self.client.get("/TestUser3/follow")
        response = self.client.get("/follow/")
        self.assertContains(response, "Test post")

    def test_news_lent(self):
        """Новая запись пользователя не появляется в ленте тех, кто не подписан на него"""
        self.client.get("/TestUser3/follow")
        response = self.client.get("/follow/")
        self.client.logout()
        self.client.login(username="TestUser2", password="text2super3")
        response = self.client.get("/follow/")
        self.assertNotContains(response, "Test post")
