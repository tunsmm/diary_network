from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

class Group(models.Model):
    title = models.CharField(max_length=63)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_posts")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_posts",
                              blank=True, null=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    text = models.TextField()
    created = models.DateTimeField("date commented", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
