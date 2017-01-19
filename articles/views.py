from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Article
from django.urls import reverse
from .forms import CommentForm, NewArticleForm
import datetime


def index(request):
    latest_articles_list = Article.objects.order_by('-pub_date')[:10]
    context = {'latest_articles_list': latest_articles_list}
    return render(request, 'articles/index.html', context)


def personal(request):
    return HttpResponse("It is your personal page.")


def new_article(request):
    article = Article(pub_date=datetime.datetime.now())
    form = NewArticleForm(request.POST if request.method == 'POST' else None,
                          instance=article)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse(
            'articles:article_discussion', args=(article.id,)))
    else:
        return render(request, 'articles/new_article.html', {
            'form': form
        })


def article_discussion(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    form = CommentForm(request.POST if request.method == 'POST' else None)

    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.save()
        return HttpResponseRedirect(
            reverse('articles:article_discussion', args=(article.id,)))
    else:
        return render(request, 'articles/article_discussion.html', {
            'article': article,
            'form': form
        })
