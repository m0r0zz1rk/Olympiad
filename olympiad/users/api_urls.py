from django.urls import path

from users.api_views import AppsListViewSet, \
    AppsCUDViewSet, AppsUploadViewSet, AppsDownloadViewSet

urlpatterns = [
    path('apps/', AppsListViewSet.as_view({'get': 'list'})),
    path('app/<int:pk>/', AppsListViewSet.as_view({'get': 'retrieve'})),
    path('app_new/', AppsCUDViewSet.as_view({'post': 'create'})),
    path('app_delete/<int:app_id>/', AppsCUDViewSet.as_view({'delete': 'destroy'})),
    path('app_edit/<int:pk>/', AppsCUDViewSet.as_view({'patch': 'update'})),
    path('apps_upload/', AppsUploadViewSet.as_view({'put': 'GetAppsFromFile'})),
    path('apps_download/', AppsDownloadViewSet.as_view({'post': 'GetFile'}))
]