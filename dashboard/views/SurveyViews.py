from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from dashboard.serializers.SurveySerializers import CreateSurveySerializer, PublishSurveySerializer
from dashboard.services.SurveyService import SurveyService


class CreateSurveyView(generics.CreateAPIView):
    serializer_class = CreateSurveySerializer


class PublishSurveyView(generics.UpdateAPIView):
    serializer_class = PublishSurveySerializer

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        survey_id = request.data.get('id')

        # Validate survey and initial the survey
        survey_service = SurveyService()
        set_survey_response = survey_service.set_survey(survey_id)
        if set_survey_response:
            return Response(set_survey_response.get_json_response(), status=set_survey_response.status_code)

        # Update Survey
        serializer = self.get_serializer(survey_service.get_survey(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)