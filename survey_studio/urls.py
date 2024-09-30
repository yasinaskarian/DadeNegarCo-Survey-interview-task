from django.urls import path
from survey_studio.views.QuestionViews import SurveyUpdateQuestionsAPIView, SurveyGetQuestionsAPIView

urlpatterns = [
    path('survey/update/questions/', SurveyUpdateQuestionsAPIView.as_view(), name='survey-update-questions'),
    path('survey/get/questions/', SurveyGetQuestionsAPIView.as_view(), name='survey-get-questions'),
]
