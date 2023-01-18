import datetime

from rest_framework import filters, status, renderers
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from admins.permissions import IsAdministrator
from authen.serializers import AppsSerializer
from users.applications.check_date import CheckAppDateSave
from users.applications.create_identiier import CreateIdentifier
from users.models import Apps, Profiles
from users.permissions import IsUser
from users.applications.xlsx import UploadAppsFromExcel, DownloadApps


class PassthroughRenderer(renderers.BaseRenderer):
    """Return data as-is. View should supply a Response."""
    media_type = ''
    format = ''

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class AppsListViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка всех заявок пользователя"""
    permission_classes = [permissions.IsAuthenticated, IsUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        'date_create',
        'surname',
        'name',
        'study_year',
        'study_kind',
        'study_duration',
        'group',
        'identifier',
    ]
    serializer_class = AppsSerializer

    def get_queryset(self):
        profile = get_object_or_404(
            queryset=Profiles.objects.all(),
            dj_user_id=self.request.user.id
        )
        qs = Apps.objects.filter(contact_person_id=profile.id)
        if 'data_create' in self.request.GET:
            qs = qs.filter(date_create=self.request.GET.get('data_create'))
        if 'surname' in self.request.GET:
            qs = qs.filter(surname__contains=self.request.GET.get('surname'))
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


class AppsCUDViewSet(viewsets.ModelViewSet):
    """Добвление/обновление/удаление заявок"""
    permission_classes = [permissions.IsAuthenticated, IsUser | IsAdministrator]
    serializer_class = AppsSerializer
    queryset = Apps.objects.all()

    def create(self, request, *args, **kwargs):
        if CheckAppDateSave(datetime.date.today()):
            profile = get_object_or_404(
                queryset=Profiles.objects.all(),
                dj_user_id=request.user.id
            )
            draft_request_data = request.data.copy()
            draft_request_data['date_create'] = datetime.date.today().strftime('%d.%m.%Y')
            draft_request_data['contact_person'] = profile.id
            draft_request_data['identifier'] = CreateIdentifier()
            serialize = self.serializer_class(data=draft_request_data)
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                return Response(
                    {'success': 'Заявка успешно добавлена'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': serialize.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'error': 'Подача заявки осуществляется вне сроков подачи заявок'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        app = get_object_or_404(
            queryset=self.queryset,
            pk=self.kwargs['pk']
        )
        serialize = self.serializer_class(
            instance=app,
            data=request.data,
            partial=True
        )
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            return Response(
                {'success': 'Заявка успешно изменена'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': serialize.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        app = get_object_or_404(
            queryset=self.queryset,
            pk=self.kwargs['app_id']
        )
        try:
            app.delete()
            return Response(
                {'success': 'Заявка успешно удалена'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при удалении заявки. Повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class AppsUploadViewSet(viewsets.ViewSet):
    """Получение заявок из файла xlsx"""
    permission_classes = [permissions.IsAuthenticated, IsUser]

    def GetAppsFromFile(self, request):
        if CheckAppDateSave(datetime.date.today()):
            try:
                file = request.FILES.get('file')
            except BaseException:
                return Response(
                    {'error': 'Ошибка при получении файла. Повторите попытку или выберите другой файл'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            profile = get_object_or_404(
                queryset=Profiles.objects.all(),
                dj_user_id=self.request.user.id
            )
            d = UploadAppsFromExcel(file, profile.id)
            if 'error' in d.keys():
                return Response(
                    {'error': d['error']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {'success': 'Заявки успешно загружены'},
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'error': 'Подача заявок осуществляется вне сроков подачи заявок'},
                status=status.HTTP_400_BAD_REQUEST
            )

class AppsDownloadViewSet(viewsets.ViewSet):
    """Скачивание файла заявок с поисковыми параметрами пользователя"""
    permission_classes = [permissions.IsAuthenticated, IsUser]

    @action(methods=['post'],
            detail=True,
            renderer_classes=(PassthroughRenderer,))
    def GetFile(self, request):
        try:
            search_string = request.data['search']
        except BaseException:
            return Response(
                {'error': 'Не получена поисковая строка, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )
        profile = get_object_or_404(
            queryset=Profiles.objects.all(),
            dj_user_id=request.user.id
        )
        return DownloadApps(profile.id, search_string)
