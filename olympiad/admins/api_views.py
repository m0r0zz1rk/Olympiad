from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets, permissions, filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from admins.permissions import IsAdministrator
from admins.seriazliers import AdminProfilesSerializer, AdminAppsSerializer
from admins.service.change_pass import ChangeUserPassword
from admins.service.change_role import ChangeUserRole
from admins.service.delete_apps import DeleteUserApps
from authen.serializers import ProfileSerializer
from users.models import Profiles, Apps


class UsersListViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка пользователей/конкретного пользователя"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        'surname',
        'name',
        'patronymic',
        'position',
        'phone',
        'study_duration',
        'group',
        'identifier',
    ]
    serializer_class = AdminProfilesSerializer

    def get_queryset(self):
        qs = Profiles.objects.all()
        if 'surname' in self.request.GET:
            qs = qs.filter(surname__contains=self.request.GET.get('surname'))
        if 'name' in self.request.GET:
            qs = qs.filter(name__contains=self.request.GET.get('name'))
        if 'patronymic' in self.request.GET:
            qs = qs.filter(patronymic__contains=self.request.GET.get('name'))
        if 'oo_fullname' in self.request.GET:
            qs = qs.filter(oo_fullname__contains=self.request.GET.get('oo_fullname'))
        if 'oo_address' in self.request.GET:
            qs = qs.filter(oo_address__contains=self.request.GET.get('oo_address'))
        if 'position' in self.request.GET:
            qs = qs.filter(position__contains=self.request.GET.get('position'))
        if 'phone' in self.request.GET:
            qs = qs.filter(phone=self.request.GET.get('phone'))
        return qs


class UsersUDListViewSet(viewsets.ModelViewSet):
    """Обновление/удаление пользователей"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = ProfileSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            DeleteUserApps(self.kwargs['pk'])
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при удалении заявок пользователя, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )
        profile = get_object_or_404(
            queryset=Profiles.objects.all(),
            pk=self.kwargs['pk']
        )
        profile.delete()
        return Response(
            {'success': 'Пользователь успешно удален'},
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        profile = get_object_or_404(
            queryset=Profiles.objects.all(),
            pk=self.kwargs['pk']
        )
        try:
            check = ChangeUserRole(request.data['role'], self.kwargs['pk'])
            if check is False:
                return Response(
                    {'error': 'Невозможно изменить роль - в системе должен быть как минимум один администратор'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при смене роли пользователя, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )
        dj_user = get_object_or_404(
            queryset=User.objects.all(),
            pk=profile.dj_user_id
        )
        dj_user.email = request.data['email']
        dj_user.save()
        serialize = self.serializer_class(
            instance=profile,
            data=request.data,
            partial=True
        )
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            return Response(
                {'success': 'Информация о пользователе успешно обновлена'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Произошла ошибка при обновлении данных, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def change_password(self, request):
        user = get_object_or_404(
            queryset=User.objects.all(),
            pk=Profiles.objects.get(id=self.kwargs['pk']).dj_user_id
        )
        try:
            ChangeUserPassword(user.id, request.data['passw'])
            return Response(
                {'success': 'Пароль пользователя успешно изменен'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при смене пароля, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class AppsListViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка всех заявок пользователей/конкретной заявки"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        'date_create',
        'study_kind',
    ]
    serializer_class = AdminAppsSerializer

    def get_queryset(self):
        qs = Apps.objects.all()
        if 'date_create' in self.request.GET:
            qs = qs.filter(date_create=self.request.GET.get('date_create'))
        if 'surname' in self.request.GET:
            qs = qs.filter(surname__contains=self.request.GET.get('surname'))
        if 'user' in self.request.GET:
            ids_list = []
            profiles = Profiles.objects.filter(
                Q(surname__contains=self.request.GET.get('user'))|\
                Q(name__contains=self.request.GET.get('user'))|\
                Q(patronymic__contains=self.request.GET.get('user'))
            )
            for prof in profiles:
                ids_list.append(prof.id)
            qs = qs.filter(contact_person_id__in=ids_list)
        if 'name' in self.request.GET:
            qs = qs.filter(name__contains=self.request.GET.get('name'))
        if 'age' in self.request.GET:
            qs = qs.filter(age=int(self.request.GET.get('age')))
        if 'study_year' in self.request.GET:
            qs = qs.filter(study_year=int(self.request.GET.get('name')))
        if 'study_kind' in self.request.GET:
            qs = qs.filter(study_kind=self.request.GET.get('study_kind'))
        if 'teacher' in self.request.GET:
            qs = qs.filter(teacher__contains=self.request.GET.get('teacher'))
        if 'study_duration' in self.request.GET:
            qs = qs.filter(study_duration=int(self.request.GET.get('study_duration')))
        if 'group' in self.request.GET:
            qs = qs.filter(group__contains=self.request.GET.get('group'))
        if 'identifier' in self.request.GET:
            qs = qs.filter(identifier__contains=self.request.GET.get('identifier'))
        return qs






