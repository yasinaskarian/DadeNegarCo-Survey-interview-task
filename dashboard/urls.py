from django.urls import path
from dashboard.views.SurveyViews import CreateSurveyView, PublishSurveyView
from dashboard.views.ReportsViews.AnswersRawDatasViews import SurveyRawAnswersDataView

urlpatterns = [
    path('survey/create/', CreateSurveyView.as_view(), name='create-survey'),
    path('survey/publish/', PublishSurveyView.as_view(), name='publish-survey'),

    path('survey/raw/answers/', SurveyRawAnswersDataView.as_view(), name='survey-answers'),

]
