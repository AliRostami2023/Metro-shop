from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from blog.models import Article, Comment


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


class BlogDetail(View):
    template_name = 'blog/blog-detail.html'

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        return render(request, self.template_name, {'article': article})

    @method_decorator(login_required)
    def post(self, request: HttpRequest, slug):
        article = get_object_or_404(Article, slug=slug)

        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        Comment.objects.create(body=body, article=article, user=request.user, parent_id=parent_id)
        return render(request, self.template_name, {'article': article})
