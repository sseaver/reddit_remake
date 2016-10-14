from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class Subreddit(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    creation_time = models.DateTimeField(auto_now_add=True)

    def current_count(self):
        return Post.objects.filter(relation_subreddit=self).count()

    def today_count(self):
        return Post.objects.filter(creation_time__gt=self.creation_time + datetime.timedelta(hours=-24)).count()

    def daily_average(self):
        past_week = Post.objects.filter(creation_time__gt=self.creation_time + datetime.timedelta(days=-7)).count()
        return round((past_week / 7), 2)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)
    relation_subreddit = models.ForeignKey(Subreddit)
    relation_user = models.ForeignKey(User)

    def is_recent(self):
        now = timezone.now()
        if self.creation_time >= now + datetime.timedelta(hours=-24):
            return True
        else:
            return False

    def is_hot(self):
        now = timezone.now()
        post_comments = Comment.objects.filter(relation_post=self)
        hot_comments = []
        for item in post_comments:
            if item.creation_time >= now + datetime.timedelta(hours=-3):
                hot_comments.append(item)
        if len(hot_comments) >= 3:
            return True
        else:
            return False

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-creation_time",)


class Comment(models.Model):
    content = models.CharField(max_length=255)
    relation_user = models.ForeignKey(User)
    relation_post = models.ForeignKey(Post)
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ("-creation_time",)


class Profile(models.Model):
    user = models.OneToOneField('auth.User')
    random_fact = models.CharField(max_length=100, null=True)


@receiver(post_save, sender='auth.User')
def create_user_profile(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        Profile.objects.create(user=instance)
