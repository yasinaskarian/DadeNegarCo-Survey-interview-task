from django.urls import path
from survey_respondent.views.RespindentView import RespondentGoNextAPIView, RespondentGetCurrentAPIView

urlpatterns = [
    path('go/next/', RespondentGoNextAPIView.as_view(), name='survey-update-questions'),
    path('get/current/', RespondentGetCurrentAPIView.as_view(), name='survey-current-questions'),

]
