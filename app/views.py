from django.shortcuts import render
from app.models import Comment, Post, Subreddit
# Create your views here.


def index_view(request):

    return render(request, "index.html")


def subreddit_view(request):
    context = {
        "all_subs": Subreddit.objects.all()

    }

    return render(request, "subreddit.html", context)
