from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.exceptions import ValidationError

from survey_respondent.services.RespondentService import RespondentService
from survey_respondent.serializers.QuestionSerializer import QuestionSerializer


class RespondentGoNextAPIView(APIView):

    def post(self, request):
        try:
            respondent_service = RespondentService(request.data.get('user_id'), request.data.get('survey_id'))
            next_question = respondent_service.submit_answer_go_next(request.data.get('answer', None))
        except ValidationError as e:
            return Response({'errors': e.messages}, status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionSerializer(next_question)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RespondentGetCurrentAPIView(APIView):

    def get(self, request):

        respondent_service = RespondentService(request.query_params.get('user_id'), request.query_params.get('survey_id'))
        current_question = respondent_service.get_current_question()

        serializer = QuestionSerializer(current_question)
        return Response(serializer.data, status=status.HTTP_200_OK)