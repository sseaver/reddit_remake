from django import forms
from app.models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        fields = ("content",)
        model = Comment


class PostForm(forms.ModelForm):
    class Meta:
        fields = ("title", "content", "url")
        model = Post
