from django.urls import path

from authen.api_views import RegistrationViewSet, auth_login, check_admin, check_auth, ProfileInfoViewSet, \
    MainPageOlympiadsListViewSet, participant_login, ProfileChangeViewSet

urlpatterns = [
    path('registration/', RegistrationViewSet.as_view({'post': 'registration'})),
    path('profile/', ProfileInfoViewSet.as_view({'get': 'user_info'})),
    path('profile_update/', ProfileChangeViewSet.as_view({'patch': 'UpdateInfo'})),
    path('password_update/', ProfileChangeViewSet.as_view({'patch': 'ChangePass'})),
    path('login/', auth_login, name='login'),
    path('participant_login/', participant_login, name='participant_login'),
    path('check_admin/', check_admin, name='check_admin'),
    path('check_auth/', check_auth, name='check_auth'),
    path('mainpage_olympiads/', MainPageOlympiadsListViewSet.as_view({'get': 'list'}))
]
