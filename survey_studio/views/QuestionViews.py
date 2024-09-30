from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from survey_studio.serializers.QuestionSerializers.QuestionUpdateMethodSerializer import QuestionUpdateMethodSerializers
from survey_studio.serializers.QuestionSerializers.QuestionGetMethodSerializer import QuestionGetMethodSerializer
from django.core.exceptions import ValidationError
from dashboard.models.Survey import Survey
from dashboard.services.SurveyService import SurveyService

class SurveyUpdateQuestionsAPIView(APIView):

    def post(self, request):
        serializer = QuestionUpdateMethodSerializers(data=request.data)
        try:
            if serializer.is_valid():
                serializer.create(serializer.validated_data)

                return Response({"message": "Questions updated successfully."}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'errors': e.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SurveyGetQuestionsAPIView(APIView):

    def get(self, request):
        try:
            survey_service = SurveyService()
            set_survey_response = survey_service.set_survey(request.query_params.get('survey_id'))
            if set_survey_response:
                return Response(set_survey_response.get_json_response(), status=set_survey_response.status_code)
            serializer = QuestionGetMethodSerializer(survey_service.get_survey())
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Survey.DoesNotExist:
            return Response({'error': 'Survey not found'}, status=status.HTTP_404_NOT_FOUND)