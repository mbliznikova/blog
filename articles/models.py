from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
from django.utils import timezone


@python_2_unicode_compatible
class Article(models.Model):
    article_header = models.CharField(max_length=100, default='No subject',
                                      unique=True)
    article_text = models.CharField(max_length=100000)
    pub_date = models.DateTimeField()
    author = models.CharField(max_length=50)

    def __str__(self):
        return self.article_header

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=3)


@python_2_unicode_compatible
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200, default='')
    author = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.comment_text
