from django.conf.urls import url, include
from django.contrib import admin
from app.views import (index_view, AllSubredditView, SubredditView, PostView,
                       SubredditUpdateView, SubredditCreateView, PostCreateView,
                       PostUpdateView, UserCreateView, CommentUpdateView)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', index_view, name="index_view"),
    url(r'^create_user/$', UserCreateView.as_view(), name="user_create_view"),
    url(r'^subreddits/$', AllSubredditView.as_view(), name="all_subreddit_view"),
    url(r'^subreddits/(?P<pk>\d+)/$', SubredditView.as_view(), name="subreddit_view"),
    url(r'^subreddits/create/$', SubredditCreateView.as_view(), name="subreddit_create_view"),
    url(r'^subreddits/(?P<pk>\d+)/update/$', SubredditUpdateView.as_view(), name="subreddit_update_view"),
    url(r'^post/(?P<pk>\d+)/$', PostView.as_view(), name="post_view"),
    url(r'^subreddits/(?P<pk>\d+)/post/create/$', PostCreateView.as_view(), name="post_create_view"),
    url(r'^post/(?P<pk>\d+)/update/$', PostUpdateView.as_view(), name="post_update_view"),
    url(r'^comment/(?P<pk>\d+)/update/$', CommentUpdateView, name="comment_update_view")

]
