from django.conf.urls import url

from . import views

app_name = 'articles'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^personal/$', views.personal, name='personal'),
    url(r'^new_article/$', views.new_article, name='new_article'),
    url(r'^(?P<article_id>[0-9]+)/article_discussion/$',
        views.article_discussion,
        name='article_discussion'),
]
