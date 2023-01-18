from django.contrib import admin

from users.models import Profiles


@admin.register(Profiles)
class ProfilesAdmin(admin.ModelAdmin):
    pass
