from django.urls import path

from participants.api_views import ParticipantInfoViewSet, OlympiadInfoViewSet, OlympiadStart, \
    ParticipantQuestionsListViewSet, QuestionsListViewSet, ParticipantAnswerViewSet, OlympiadStop, \
    ParticipantRemainigTimeViewSet, DetectClosePage

urlpatterns = [
    path('participant_info/', ParticipantInfoViewSet.as_view({'post': 'retrieve'})),
    path('olympiad_info/', OlympiadInfoViewSet.as_view({'post': 'retrieve'})),

    path('olympiad_start/', OlympiadStart.as_view({'post': 'OlympiadStart'})),
    path('olympiad_stop/', OlympiadStop.as_view({'post': 'OlympiadStop'})),

    path('get_time/', ParticipantRemainigTimeViewSet.as_view({'post': 'GetRemainingTime'})),

    path('participant_questions/', ParticipantQuestionsListViewSet.as_view({'post': 'GetQuestions'})),

    path('question_cols/', QuestionsListViewSet.as_view({'post': 'GetColumns'})),
    path('question_rows/', QuestionsListViewSet.as_view({'post': 'GetRows'})),

    path('get_table/', ParticipantAnswerViewSet.as_view({'post': 'GetTableAnswers'})),
    path('save_table/', ParticipantAnswerViewSet.as_view({'post': 'SaveTableAnswer'})),
    path('get_simple/', ParticipantAnswerViewSet.as_view({'post': 'TakeSimpleAnswers'})),
    path('save_detailed/', ParticipantAnswerViewSet.as_view({'post': 'SaveDetailedAnswer'})),
    path('get_short/', ParticipantAnswerViewSet.as_view({'post': 'TakeShortAnswers'})),
    path('save_short/', ParticipantAnswerViewSet.as_view({'post': 'SaveShortAnswer'})),
    path('take_possible/', ParticipantAnswerViewSet.as_view({'post': 'TakePossibleValues'})),
    path('take_acc_labels/', ParticipantAnswerViewSet.as_view({'post': 'TakeAccordanceLabels'})),
    path('take_acc_answers/', ParticipantAnswerViewSet.as_view({'post': 'TakeAccordanceAnswers'})),
    path('save_acc/', ParticipantAnswerViewSet.as_view({'post': 'SaveAccordanceAnswer'})),
    path('take_choices/', ParticipantAnswerViewSet.as_view({'post': 'TakeChoicesAnswers'})),
    path('take_part_choices/', ParticipantAnswerViewSet.as_view({'post': 'TakeParticipantChoices'})),
    path('save_choice/', ParticipantAnswerViewSet.as_view({'post': 'SaveChoice'})),

    path('close_page/', DetectClosePage, name="DetectClosePage")
]