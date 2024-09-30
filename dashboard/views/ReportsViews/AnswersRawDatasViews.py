from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from survey_respondent.models.Answers import (
    YesNoAnswer,
    MultipleChoiceAnswer,
    RankingAnswer,
    MatrixAnswer
)
from dashboard.serializers.ReportsSerializer.AnswersRawDatasSerializers import (YesNoAnswerSerializer,
                                                                                MultipleChoiceAnswerSerializer,
                                                                                RankingAnswerSerializer,
                                                                                MatrixAnswerSerializer)
class SurveyRawAnswersDataView(APIView):
    def get(self, request):
        survey_id = request.query_params.get('survey_id')
        order_value = request.query_params.get('order_value')

        if not survey_id or not order_value:
            return Response({"error": "survey_id and order_value are required."}, status=status.HTTP_400_BAD_REQUEST)

        answers = {
            'yes_no_answers': YesNoAnswer.objects.filter(
                question__survey_id=survey_id
            ).order_by('created_at'),
            'multiple_choice_answers': MultipleChoiceAnswer.objects.filter(
                question__survey_id=survey_id
            ).order_by('created_at'),
            'ranking_answers': RankingAnswer.objects.filter(
                question__survey_id=survey_id
            ).order_by('created_at'),
            'matrix_answers': MatrixAnswer.objects.filter(
                question__survey_id=survey_id
            ).order_by('created_at'),
        }

        # Filter answers based on the provided order_value
        filtered_answers = {}
        for key, queryset in answers.items():
            filtered_answers[key] = queryset.filter(question__order=order_value)

        # Serialize the answers
        response_data = {
            'yes_no_answers': YesNoAnswerSerializer(filtered_answers['yes_no_answers'], many=True).data,
            'multiple_choice_answers': MultipleChoiceAnswerSerializer(filtered_answers['multiple_choice_answers'], many=True).data,
            'ranking_answers': RankingAnswerSerializer(filtered_answers['ranking_answers'], many=True).data,
            'matrix_answers': MatrixAnswerSerializer(filtered_answers['matrix_answers'], many=True).data,
        }
        filtered_response_data = {key: value for key, value in response_data.items() if value}

        return Response(filtered_response_data, status=status.HTTP_200_OK)
