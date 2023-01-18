from django.urls import path

from service.api_views import LevelsListViewSet, LevelsCUDViewSet, QuestionsListViewSet, QuestionsImagesUploadViewSet, \
    QuestionAddViewSet, QuestionColumnsListViewSet, QuestionColumnCDViewSet, TableAnswersListViewSet, \
    TableAnswersCDViewSet, TableAnswerViewSet, QuestionDeleteViewSet, ShortAnswerViewSet, QuestionEditViewSet, \
    ChoiceAnswerViewSet, AccordanceChoiceViewSet, AccAnswersViewSet, AccReadViewSet, OlympiadsListViewSet, \
    OlympiadsCUDViewSet, OlympiadsLevelsListViewSet, OlympiadLevelsCDViewSet, ResultsOlympiadsListViewSet, \
    ResultsActionsViewSet, ResultsCompletesListViewSet, GetOlympiadTheme, ResultQuestionsListViewSet, \
    DetailResultActionsViewSet

urlpatterns = [
    path('levels/', LevelsListViewSet.as_view({'get': 'list'})),
    path('level/<int:pk>/', LevelsListViewSet.as_view({'get': 'retrieve'})),
    path('level_new/', LevelsCUDViewSet.as_view({'post': 'create'})),
    path('level_delete/<int:pk>/', LevelsCUDViewSet.as_view({'delete': 'destroy'})),
    path('level_update/<int:pk>/', LevelsCUDViewSet.as_view({'patch': 'update'})),

    path('questions/', QuestionsListViewSet.as_view({'get': 'list'})),
    path('question/<int:pk>/', QuestionsListViewSet.as_view({'get': 'retrieve'})),
    path('question_new/', QuestionAddViewSet.as_view({'post': 'create'})),
    path('question_update/<int:pk>/', QuestionEditViewSet.as_view({'put': 'EditQuestion'})),
    path('question_delete/<int:pk>/', QuestionDeleteViewSet.as_view({'delete': 'destroy'})),

    path('question_columns/', QuestionColumnsListViewSet.as_view({'get': 'list'})),
    path('column_new/', QuestionColumnCDViewSet.as_view({'post': 'create'})),
    path('column_delete/<int:pk>/', QuestionColumnCDViewSet.as_view({'delete': 'destroy'})),
    path('question_rows/', TableAnswersListViewSet.as_view({'get': 'list'})),
    path('row_new/', TableAnswersCDViewSet.as_view({'post': 'create'})),
    path('row_delete/', TableAnswersCDViewSet.as_view({'post': 'destroy'})),

    path('get_short/', ShortAnswerViewSet.as_view({'get': 'GetAnswer'})),
    path('short_signature/', ShortAnswerViewSet.as_view({'post': 'SetSignature'})),
    path('short_correct/', ShortAnswerViewSet.as_view({'post': 'SetAnswer'})),

    path('choices/', ChoiceAnswerViewSet.as_view({'get': 'list'})),
    path('choice_add/', ChoiceAnswerViewSet.as_view({'post': 'create'})),
    path('choice_delete/<int:pk>/', ChoiceAnswerViewSet.as_view({'delete': 'destroy'})),
    path('set_choice/', ChoiceAnswerViewSet.as_view({'put': 'update'})),

    path('accs/', AccordanceChoiceViewSet.as_view({'get': 'list'})),
    path('acc_add/', AccordanceChoiceViewSet.as_view({'post': 'create'})),
    path('acc_delete/<int:pk>/', AccordanceChoiceViewSet.as_view({'delete': 'destroy'})),

    path('acc_answers/', AccReadViewSet.as_view({'get': 'list'})),
    path('acc_answer_add/', AccAnswersViewSet.as_view({'post': 'create'})),
    path('acc_answer_delete/<int:pk>/', AccAnswersViewSet.as_view({'delete': 'destroy'})),

    path('answers/', TableAnswerViewSet.as_view({'post': 'GetAnswers'})),
    path('set_answer/', TableAnswerViewSet.as_view({'post': 'SetAnswer'})),

    path('upload_image/', QuestionsImagesUploadViewSet.as_view({'put': 'ImageUpload'})),

    path('olympiads/', OlympiadsListViewSet.as_view({'get': 'list'})),
    path('olympiad/<int:pk>/', OlympiadsListViewSet.as_view({'get': 'retrieve'})),
    path('olympiad_new/', OlympiadsCUDViewSet.as_view({'post': 'create'})),
    path('olympiad_update/<int:pk>/', OlympiadsCUDViewSet.as_view({'put': 'update'})),
    path('olympiad_delete/<int:pk>/', OlympiadsCUDViewSet.as_view({'delete': 'destroy'})),

    path('olympiads_levels/', OlympiadsLevelsListViewSet.as_view({'get': 'list'})),
    path('olympiad_levels/<int:pk>/', OlympiadsLevelsListViewSet.as_view({'get': 'retrieve'})),
    path('olympiad_level_add/', OlympiadLevelsCDViewSet.as_view({'post': 'create'})),
    path('olympiad_level_delete/<int:pk>/', OlympiadLevelsCDViewSet.as_view({'delete': 'destroy'})),

    path('results_olympiads/', ResultsOlympiadsListViewSet.as_view({'get': 'list'})),
    path('results_download/<int:olympiad_id>/', ResultsActionsViewSet.as_view({'get': 'GetFile'})),

    path('olympiad_theme/', GetOlympiadTheme, name="GetOlympiadTheme"),
    path('results_completes/', ResultsCompletesListViewSet.as_view({'get': 'list'})),

    path('result_questions/<str:id>/', ResultQuestionsListViewSet.as_view({'get': 'GetQuestions'})),
    path('result_get_lastfirstname/<str:id>/', DetailResultActionsViewSet.as_view({'get': 'GetLastFirstName'})),
    path('result_get_classic/<str:id>/', DetailResultActionsViewSet.as_view({'get': 'GetClassicAnswers'})),
    path('result_get_acc/<str:id>/', DetailResultActionsViewSet.as_view({'get': 'GetAccAnswers'})),
    path('result_get_short/<str:id>/', DetailResultActionsViewSet.as_view({'get': 'GetShortAnswers'})),
    path('result_get_detailed/<str:id>/', DetailResultActionsViewSet.as_view({'get': 'GetDetailedAnswers'})),
    path('result_get_table/<str:id>/', DetailResultActionsViewSet.as_view({'get': 'GetTableAnswers'})),

    path('result_save_classic_detail/', DetailResultActionsViewSet.as_view({'post': 'SaveClassicDetailPoints'})),
    path('result_save_acc_table_short/', DetailResultActionsViewSet.as_view({'post': 'SaveShortAccTablePoints'})),

    path('result_recount/<str:identifier>/', DetailResultActionsViewSet.as_view({'get': 'RecountParticipantResult'})),

    path('recount_olympiad/<int:olympiad_id>/', ResultsActionsViewSet.as_view({'get': 'CountingResults'})),
]