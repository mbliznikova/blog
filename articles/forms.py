from django import forms
from .models import Article, Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'comment_text')


class NewArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('article_header', 'article_text', 'author')
