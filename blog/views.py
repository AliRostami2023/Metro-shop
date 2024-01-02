from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Article


# Create your views here.


class BlogList(ListView):
    template_name = 'blog/blog-list.html'
    model = Article
    paginate_by = 8
    context_object_name = 'articles'

    def get_queryset(self):
        query = super().get_queryset()
        category_name = self.kwargs.get('cat')

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query


class BlogDetail(DetailView):
    template_name = 'blog/blog-detail.html'
    model = Article
    context_object_name = 'article'
