from django.shortcuts import render
from app.models import Comment, Post, Subreddit, Profile
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.forms import CommentForm, PostForm
from django.urls import reverse, reverse_lazy

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


class SubredditCreateView(CreateView):
    model = Subreddit
    success_url = "/subreddits"
    fields = ("name", "description")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.relation_user = self.request.user
        return super().form_valid(form)


class SubredditUpdateView(UpdateView):
    model = Subreddit
    success_url = "/subreddits"
    fields = ("name", "description")


class PostView(CreateView):
    model = Comment
    fields = ("content",)
    template_name = "app/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.get(id=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.relation_user = self.request.user
        instance.relation_post = Post.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.kwargs['pk']
        return "/post/{}/".format(post_id)


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.relation_user = self.request.user
        instance.relation_subreddit = Subreddit.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        subreddit_id = self.kwargs['pk']
        return "/subreddits/{}/".format(subreddit_id)


class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'content', 'url')

    def get_success_url(self):
        post_id = self.kwargs['pk']
        return "/post/{}/".format(post_id)


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ("content",)
    success_url = reverse_lazy("post_view")

    # def get_success_url(self):
    #     return "/subreddits/"


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)
