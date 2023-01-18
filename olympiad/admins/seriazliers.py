from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Profiles, Apps


class AdminProfilesSerializer(serializers.ModelSerializer):
    """Сериализация профилей пользователей с добавчным полем роли"""
    role = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        return User.objects.get(id=obj.dj_user_id).email

    def get_role(self, obj):
        if User.objects.get(id=obj.dj_user_id).groups.filter(name='Администраторы').exists():
            return 'Администратор'
        else:
            return 'Пользователь'

    class Meta:
        model = Profiles
        exclude = ('dj_user',)


class AdminAppsSerializer(serializers.ModelSerializer):
    """Сериализация заявок всех пользователей"""
    profile = serializers.SerializerMethodField()

    class Meta:
        model = Apps
        exclude = ('contact_person',)

    def get_profile(self, obj):
        return f'{obj.contact_person.surname} {obj.contact_person.name} {obj.contact_person.patronymic}'