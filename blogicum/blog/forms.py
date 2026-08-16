from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'image', 'pub_date', 'location', 'category')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
