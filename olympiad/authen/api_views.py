import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from admins.service.change_pass import ChangeUserPassword
from authen.login.phone_to_username import GetUsernameByPhone
from authen.login.user_data import GetFIOLoginedUser
from authen.participant.create_session import CreateParticipantSession
from authen.registration.add_to_group import AddUserToGroup
from authen.registration.login import CreateUserLogin
from authen.registration.save_user import SaveNewUser
from authen.serializers import ProfileRegistrationSerializer, ProfileSerializer, RegistrationSerializer
from authen.services.auth import AuthBackend
from authen.services.token import JWTToken
from participants.models import Sessions
from service.models import Olympiads, ResultsSessions
from service.serializers import OlympiadsSerializer
from users.models import Profiles, Apps


@api_view(['GET'])
def check_auth(request):
    """Проверка авторизации пользователя"""
    auth = AuthBackend()
    data = auth.authenticate(request=request)
    if data is not None:
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@login_required
def check_admin(request):
    """Проверка пользователя на права администратора"""
    if request.user.groups.filter(name='Администраторы').exists():
        return JsonResponse({'is_admin': True})
    else:
        return JsonResponse({'is_admin': False})


@api_view(['POST'])
def auth_login(request):
    """Авторизация пользователя в системе"""
    try:
        data_phone = request.data.get('phone')
        data_pass = request.data.get('pass')
    except BaseException:
        return Response(
            {'error': 'Номер телефона или пароль не были предоставлены'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not Profiles.objects.filter(phone=data_phone).exists():
        if not User.objects.filter(email=data_phone).exists():
            return Response(
                {'error': 'Пользователь с указанным номером телефона/почтой не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
    user = authenticate(
        request,
        username=GetUsernameByPhone(data_phone),
        password=data_pass
    )
    if user is not None:
        auth_data = JWTToken(user.id)
        return JsonResponse({
            'token': auth_data['access_token'],
            'user_id': user.id,
            'fio': GetFIOLoginedUser(user.id)
        })
    else:
        return Response(
            {'error': 'Неправильный логин или пароль. Повторите попытку'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def participant_login(request):
    """Вход для участника олимпиады"""
    try:
        app = get_object_or_404(
            queryset=Apps.objects.all(),
            identifier=request.data['participant_id']
        )
        if Olympiads.objects.filter(date_reg_start__lte=app.date_create).\
            filter(date_reg_end__gte=app.date_create).exists():
            olympic = Olympiads.objects.filter(date_reg_start__lte=app.date_create).\
                filter(date_reg_end__gte=app.date_create)[:1].get()
            if olympic.event_date != datetime.date.today():
                if olympic.event_date > datetime.date.today():
                    return Response(
                        {'error': 'Дата проведения олимпиады еще не наступила'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                if olympic.event_date < datetime.date.today():
                    return Response(
                        {'error': 'Олимпиада уже проведена'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            if ResultsSessions.objects.filter(participant_identifier=app.identifier).exists():
                return Response(
                    {'error': 'Участник уже завершил прохождение олимпиады'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if Sessions.objects.filter(participant_id=app.identifier).exists():
                ses = get_object_or_404(
                    queryset=Sessions.objects.all(),
                    participant_id=app.identifier
                )
                if ses.time_finish > ses.time_olympic:
                    return Response(
                        {'error': 'Участник уже завершил прохождение олимпиады'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if ses.time_olympic == ses.time_startpage:
                    return Response(
                        {
                            'status': 'startpage',
                            'uuid': ses.unique_id
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'status': 'passing',
                            'uuid': ses.unique_id
                        },
                        status=status.HTTP_200_OK
                    )

            else:
                ses = CreateParticipantSession(app.identifier, olympic.id)
                return Response(
                    {
                        'status': 'startpage',
                        'uuid': ses.unique_id
                    },
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'error': 'Участник найден, но заявка была подана вне сроков подачи заявок на участие в олимпиаде'},
                status=status.HTTP_403_FORBIDDEN
            )
    except BaseException:
        return Response(
            {'error': 'Произошла ошибка при входе участника, повторите попытку позже'},
            status=status.HTTP_400_BAD_REQUEST
        )


class RegistrationViewSet(viewsets.ModelViewSet):
    """Регистрация контактного лица/администратора в системе"""
    serializer_class = ProfileRegistrationSerializer

    def registration(self, request):
        if len(request.data['passw']) < 8:
            return Response(
                {'error': 'Минимальная длина пароля - 8 символов'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.data['passw'] != request.data['passw2']:
            return Response(
                {'error': 'Введеные пароли не совпадают'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=request.data['email']).exists():
            return Response(
                {'error': 'Пользователь с таким email уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Profiles.objects.filter(phone=request.data['phone']).exists():
            return Response(
                {'error': 'Пользователь с таким номером телефон уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        check = ProfileRegistrationSerializer(data=request.data)
        if check.is_valid(raise_exception=True):
            login = CreateUserLogin(request.data['surname'], request.data['name'])
            dj_user = SaveNewUser(login, request.data['passw'], request.data['email'])
            if dj_user is False:
                return Response(
                    {'error': 'Произошла ошибка при добавлении нового пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            AddUserToGroup(dj_user)
            draft_request_data = request.data.copy()
            draft_request_data['dj_user'] = dj_user
            serialize = RegistrationSerializer(data=draft_request_data)
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                return JsonResponse({'success': 'Пользователь успешно зарегистрирован'})
            else:
                return Response(
                    {'error': serialize.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return JsonResponse(
                {'error': check.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileInfoViewSet(viewsets.ModelViewSet):
    """Получение информации о профиле пользователя"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profiles.objects.all()

    def user_info(self, request):
        profile = get_object_or_404(
            queryset=self.queryset,
            dj_user_id=request.user.id
        )
        try:
            serialize = self.serializer_class(profile)
            return Response(
                {'profile': serialize.data},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': serialize.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileChangeViewSet(viewsets.ModelViewSet):
    """Изменение информации/пароля пользователя в профиле"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def UpdateInfo(self, request):
        profile = get_object_or_404(
            queryset=Profiles.objects.all(),
            dj_user_id=request.user.id
        )
        dj_user = get_object_or_404(
            queryset=User.objects.all(),
            pk=request.user.id
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
                {'success': 'Личная информация успешно обновлена'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Произошла ошибка при обновлении данных, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def ChangePass(self, request):
        try:
            ChangeUserPassword(request.user.id, request.data['passw'])
            return Response(
                {'success': 'Пароль успешно изменен'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при смене пароля, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class MainPageOlympiadsListViewSet(viewsets.ReadOnlyModelViewSet):
    """Список предстоящих олимпиад"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OlympiadsSerializer
    queryset = Olympiads.objects.filter(event_date__gte=datetime.date.today()).order_by('event_date')





