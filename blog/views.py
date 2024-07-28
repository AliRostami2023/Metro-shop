from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from blog.models import Article, Comment, CategoryBlog


# Create your views here.


class BlogList(ListView):
    template_name = 'blog/blog-list.html'
    model = Article
    paginate_by = 8
    # context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.prefetch_related('category').select_related('author').filter(published=True)
        return context

    def get_queryset(self):
        query = super().get_queryset()
        category_name = self.kwargs.get('cat')

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query


class BlogDetail(View):
    template_name = 'blog/blog-detail.html'

    def setup(self, request, *args, **kwargs):
        self.slug = get_object_or_404(Article, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        article = self.slug
        return render(request, self.template_name, {'article': article})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        article = self.slug

        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        Comment.objects.create(body=body, article=article, user=request.user, parent_id=parent_id)
        return render(request, self.template_name, {'article': article})


def sidebar_blog_component(request):
    categories = CategoryBlog.objects.filter(parent__isnull=True)
    recent_post = Article.objects.order_by('?')[:7]
    return render(request, 'components/sidebar-blog.html', {'categories': categories, 'posts': recent_post})
