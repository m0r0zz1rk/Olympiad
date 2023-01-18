from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Profiles, Apps


class ProfileRegistrationSerializer(serializers.ModelSerializer):
    """Сериализация регистрации профиля пользователя"""
    passw = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Пароль'
    )
    passw2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Подтверждение пароля'
    )

    class Meta:
        model = Profiles
        exclude = ('dj_user',)


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализация модели профиля для регистрации пользователя"""

    class Meta:
        model = Profiles
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализация модели профиля пользовтеля"""
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        return User.objects.get(id=obj.dj_user_id).email

    class Meta:
        model = Profiles
        exclude = ('dj_user',)


class AppsSerializer(serializers.ModelSerializer):
    """Сериализация модели заявок пользователя"""

    class Meta:
        model = Apps
        fields = '__all__'
