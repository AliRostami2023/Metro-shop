from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('captcha/', include('captcha.urls')),
    path('', include('home.urls')),
    path('account/', include('account.urls')),
    path('products/', include('product.urls')),
    path('blogs/', include('blog.urls')),
    path('cart/', include('order.urls')),
    path('dashboard/', include('panel.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
