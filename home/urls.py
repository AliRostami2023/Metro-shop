from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home-page'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact-us-page'),
]

