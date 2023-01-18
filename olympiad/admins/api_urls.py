from django.urls import path

from admins.api_views import UsersListViewSet, UsersUDListViewSet, AppsListViewSet

urlpatterns = [
    path('users/', UsersListViewSet.as_view({'get': 'list'})),
    path('user/<int:pk>/', UsersListViewSet.as_view({'get': 'retrieve'})),
    path('user_delete/<int:pk>/', UsersUDListViewSet.as_view({'delete': 'destroy'})),
    path('user_update/<int:pk>/', UsersUDListViewSet.as_view({'patch': 'update'})),
    path('user_changepass/<int:pk>/', UsersUDListViewSet.as_view({'patch': 'change_password'})),

    path('apps/', AppsListViewSet.as_view({'get': 'list'})),
    path('app/<int:pk>/', AppsListViewSet.as_view({'get': 'retrieve'})),
]