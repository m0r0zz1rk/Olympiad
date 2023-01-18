from django.contrib import admin

from participants.models import Sessions, ParticipantsAnswers


@admin.register(Sessions)
class SessionsAdmin(admin.ModelAdmin):
    pass


@admin.register(ParticipantsAnswers)
class ParticipantsAnswersAdmin(admin.ModelAdmin):
    pass
