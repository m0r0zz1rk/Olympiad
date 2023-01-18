from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings

from .yasg import urlpatterns as docs_urls


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/authen/', include('authen.api_urls')),
    path('api/users/', include('users.api_urls')),
    path('api/participants/', include('participants.api_urls')),
    path('api/admins/', include('admins.api_urls')),
    path('api/service/', include('service.api_urls')),
    path('tinymce/', include('tinymce.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += docs_urls
