from django.urls import reverse
from rest_framework.test import APITestCase
from survey_studio.models.Questions import (Survey, MatrixQuestion, MultipleChoiceQuestion, RankingQuestion, YesNoQuestion)
from rest_framework import status


class SurveyGetQuestionAPITest(APITestCase):

    def setUp(self):
        # Create a survey
        self.survey = Survey.objects.create(title='Test Survey')

        # Add different types of questions in non-sequential order
        self.yes_no_question = YesNoQuestion.objects.create(
            survey=self.survey, text="Do you like pizza?", order=2
        )
        self.multiple_choice_question = MultipleChoiceQuestion.objects.create(
            survey=self.survey, text="What is your favorite color?", order=1, options=["Red", "Blue"]
        )
        self.matrix_question = MatrixQuestion.objects.create(
            survey=self.survey, text="Rate these items", order=3, rows=["Item 1", "Item 2"], columns=["Bad", "Good"]
        )
        self.ranking_question = RankingQuestion.objects.create(
            survey=self.survey, text="Rank these", order=4, options=["Option 1", "Option 2"]
        )

    def test_survey_questions_ordered_by_order(self):
        url = reverse('survey-get-questions')

        response = self.client.get(f"{url}?survey_id={self.survey.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], self.survey.id)
        self.assertEqual(response.data['title'], self.survey.title)

        expected_questions = [
            {"MultipleChoiceQuestion": {"text": "What is your favorite color?", "order": 1, "options": ["Red", "Blue"]}},
            {"YesNoQuestion": {"text": "Do you like pizza?", "order": 2}},
            {"MatrixQuestion": {"text": "Rate these items", "order": 3, "rows": ["Item 1", "Item 2"], "columns": ["Bad", "Good"]}},
            {"RankingQuestion": {"text": "Rank these", "order": 4, "options": ["Option 1", "Option 2"]}}
        ]
        print(response.data)
        self.assertEqual(response.data['questions'], expected_questions)
