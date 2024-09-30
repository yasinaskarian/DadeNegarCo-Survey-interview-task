from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from survey_studio.models.Questions import (Survey, MatrixQuestion, MultipleChoiceQuestion, RankingQuestion, YesNoQuestion)


class SurveyUpdateQuestionsTest(APITestCase):
    def setUp(self):
        # Create a survey instance for testing
        self.survey = Survey.objects.create(title=""
                                                  "Test Survey")

        self.url = reverse('survey-update-questions')

    def test_create_matrix_question(self):
        data = {
            "survey_id": self.survey.id,
            "questions": [
                {"MatrixQuestion": {"text": "What are your preferences?", "order": 1, "rows": ["Row 1", "Row 2"],
                                    "columns": ["Column 1", "Column 2"]}}
            ]
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MatrixQuestion.objects.count(), 1)

    def test_update_matrix_question(self):
        MatrixQuestion.objects.create(survey=self.survey, text="What are your preferences?", order=1, rows=["Row 1"],
                                      columns=["Column 1"])

        data = {
            "survey_id": self.survey.id,
            "questions": [
                {"MatrixQuestion": {"text": "What are your preferences?", "order": 1, "rows": ["Row 1", "Row 2"],
                                    "columns": ["Column 1", "Column 2"]}}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        question = MatrixQuestion.objects.get(order=1, survey=self.survey)
        self.assertEqual(question.rows, ["Row 1", "Row 2"])
        self.assertEqual(question.columns, ["Column 1", "Column 2"])

    def test_delete_matrix_question(self):
        MatrixQuestion.objects.create(survey=self.survey, text="What are your preferences?", order=1, rows=["Row 1"],
                                      columns=["Column 1"])

        data = {
            "survey_id": self.survey.id,
            "questions": []  # No questions means it should delete existing ones
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MatrixQuestion.objects.count(), 0)

    def test_create_multiple_choice_question(self):
        data = {
            "survey_id": self.survey.id,
            "questions": [
                {"MultipleChoiceQuestion": {"text": "Select your favorite color", "order": 1,
                                            "options": ["Red", "Blue", "Green"]}}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MultipleChoiceQuestion.objects.count(), 1)

    def test_update_multiple_choice_question(self):
        MultipleChoiceQuestion.objects.create(survey=self.survey, text="Select your favorite color", order=1,
                                              options=["Red", "Blue"])

        data = {
            "survey_id": self.survey.id,
            "questions": [
                {"MultipleChoiceQuestion": {"text": "Select your favorite color", "order": 1,
                                            "options": ["Red", "Blue", "Green"]}}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        question = MultipleChoiceQuestion.objects.get(order=1, survey=self.survey)
        self.assertEqual(question.options, ["Red", "Blue", "Green"])

    def test_delete_multiple_choice_question(self):
        MultipleChoiceQuestion.objects.create(survey=self.survey, text="Select your favorite color", order=1,
                                              options=["Red", "Blue"])

        data = {
            "survey_id": self.survey.id,
            "questions": []  # No questions means it should delete existing ones
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MultipleChoiceQuestion.objects.count(), 0)

    def test_create_ranking_question(self):
        data = {
            "survey_id": self.survey.id,
            "questions": [
                {"RankingQuestion": {"text": "Rank these fruits", "order": 1, "options": ["Apple", "Banana", "Cherry"]}}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RankingQuestion.objects.count(), 1)

    def test_update_ranking_question(self):
        RankingQuestion.objects.create(survey=self.survey, text="Rank these fruits", order=1,
                                       options=["Apple", "Banana"])

        data = {
            "survey_id": self.survey.id,
            "questions": [
                {"RankingQuestion": {"text": "Rank these fruits", "order": 1, "options": ["Apple", "Banana", "Cherry"]}}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        question = RankingQuestion.objects.get(order=1, survey=self.survey)
        self.assertEqual(question.options, ["Apple", "Banana", "Cherry"])

    def test_delete_ranking_question(self):
        RankingQuestion.objects.create(survey=self.survey, text="Rank these fruits", order=1,
                                       options=["Apple", "Banana"])

        data = {
            "survey_id": self.survey.id,
            "questions": []  # No questions means it should delete existing ones
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RankingQuestion.objects.count(), 0)

    def test_create_yes_no_question(self):
        data = {
            "survey_id": self.survey.id,
            "questions": [
                {"YesNoQuestion": {"text": "Do you like pizza?", "order": 1}}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(YesNoQuestion.objects.count(), 1)

    def test_update_yes_no_question(self):
        YesNoQuestion.objects.create(survey=self.survey, text="Do you like pizza?", order=1)

        data = {
            "survey_id": self.survey.id,
            "questions": [
                {"YesNoQuestion": {"text": "Do you like pizza?", "order": 1}}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        question = YesNoQuestion.objects.get(order=1, survey=self.survey)
        self.assertEqual(question.text, "Do you like pizza?")

    def test_delete_yes_no_question(self):
        YesNoQuestion.objects.create(survey=self.survey, text="Do you like pizza?", order=1)

        data = {
            "survey_id": self.survey.id,
            "questions": []  # No questions means it should delete existing ones
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(YesNoQuestion.objects.count(), 0)


    def test_create_multiple_questions(self):

        data = {
            "survey_id": self.survey.id,
            "questions": [
                {"RankingQuestion": {"text": "Rank these fruits", "order": 1, "options": ["Apple", "Banana", "Cherry"]}},
                {"YesNoQuestion": {"text": "Do you like pizza?", "order": 2}},
                {"YesNoQuestion": {"text": "Do you like burgers?", "order": 4}},
                {"MultipleChoiceQuestion": {"text": "Select your favorite color", "order": 1,
                                            "options": ["Red", "Blue", "Green"]}},
                {"MatrixQuestion": {"text": "What are your preferences?", "order": 1, "rows": ["Row 1", "Row 2"],
                                    "columns": ["Column 1", "Column 2"]}}

            ]
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(YesNoQuestion.objects.count(), 2)
        self.assertEqual(RankingQuestion.objects.count(), 1)
        self.assertEqual(MultipleChoiceQuestion.objects.count(), 1)
        self.assertEqual(MatrixQuestion.objects.count(), 1)
