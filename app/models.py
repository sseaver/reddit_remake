from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Subreddit(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    creation_time = models.DateTimeField(auto_now_add=True)

    def current_count(self):
        return Post.objects.all().count()

    def today_count(self):
        return Post.objects.filter(self.creation_time > datetime.timedelta(hours=-24))

    def daily_average(self):
        past_week = Post.objects.filter(self.creation_time > datetime.timedelta(days=-7))
        return round((past_week / 7), 2)

    def __str__(self):
        return str(self.name)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=255)
    url = models.URLField()
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)
    relation_subreddit = models.ForeignKey(Subreddit)
    relation_user = models.ForeignKey(User)

    def is_recent(self):
        if Post.creation_time < datetime.timedelta(hours=-24):
            return False

    def is_hot(self):
        if (Comment.creation_time > datetime.timedelta(hours=-3)).count() >= 3:
            return True

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    content = models.CharField(max_length=255)
    relation_user = models.ForeignKey(User)
    relation_post = models.ForeignKey(Post)
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
