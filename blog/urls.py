from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogList.as_view(), name='blog-list'),
    path('category/<cat>', views.BlogList.as_view(), name='category-blog'),
    path('detail/<slug:slug>', views.BlogDetail.as_view(), name='blog-detail'),
]

