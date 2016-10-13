from django.shortcuts import render
from app.models import Comment, Post, Subreddit
from django.views.generic import TemplateView, ListView, DetailView

# Create your views here.


def index_view(request):
    context = {
        "all_posts": Post.objects.all()

    }
    return render(request, "index.html", context)


class AllSubredditView(ListView):
    model = Subreddit
    template_name = "subreddits.html"


class SubredditView(DetailView):
    model = Subreddit


class PostView(DetailView):
    model = Post
