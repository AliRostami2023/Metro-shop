from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile-page'),
    path('my-shopping/', views.MyShopping.as_view(), name='shopping-page'),
    path('detail-shopping/<order_id>', views.my_shopping_detail, name='detail-my-shopping-page'),
    path('change-password/', views.ChangePasswordPanel.as_view(), name='change-password-panel-page'),
    path('edit-info/', views.EditInfoUserView.as_view(), name='edit-info-page'),
]

