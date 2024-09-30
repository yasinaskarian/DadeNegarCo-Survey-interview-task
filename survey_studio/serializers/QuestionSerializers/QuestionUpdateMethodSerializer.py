from rest_framework import serializers
from survey_studio.models.Questions import MatrixQuestion, MultipleChoiceQuestion, RankingQuestion, YesNoQuestion
from django.db.models import Value


class QuestionUpdateMethodSerializers(serializers.Serializer):
    survey_id = serializers.IntegerField()
    questions = serializers.ListField()

    def create(self, validated_data):
        survey_id = validated_data['survey_id']
        questions_data = validated_data['questions']

        # Create or update questions based on their type and order
        for question_data in questions_data:
            question_type, question_info = list(question_data.items())[0]
            question_info['survey_id'] = survey_id  # Add survey ID to the question data

            if question_type == "MatrixQuestion":
                self.__create_or_update_matrix_question(question_info)
            elif question_type == "MultipleChoiceQuestion":
                self.__create_or_update_multiple_choice_question(question_info)
            elif question_type == "RankingQuestion":
                self.__create_or_update_ranking_question(question_info)
            elif question_type == "YesNoQuestion":
                self.__create_or_update_yes_no_question(question_info)

        # Cleanup: delete questions that are no longer present
        self.__cleanup_questions(survey_id, questions_data)


    @staticmethod
    def __create_or_update_matrix_question(data):
        question, created = MatrixQuestion.objects.update_or_create(
            survey_id=data['survey_id'],
            order=data['order'],
            defaults={'text': data['text'], 'rows': data['rows'], 'columns': data['columns']}
        )

        return question

    @staticmethod
    def __create_or_update_multiple_choice_question(data):
        question, created = MultipleChoiceQuestion.objects.update_or_create(
            survey_id=data['survey_id'],
            order=data['order'],
            defaults={'text': data['text'], 'options': data['options']}
        )
        return question

    @staticmethod
    def __create_or_update_ranking_question(data):
        question, created = RankingQuestion.objects.update_or_create(
            survey_id=data['survey_id'],
            order=data['order'],
            defaults={'text': data['text'], 'options': data['options']}
        )
        return question

    @staticmethod
    def __create_or_update_yes_no_question(data):
        question, created = YesNoQuestion.objects.update_or_create(
            survey_id=data['survey_id'],
            order=data['order'],
            defaults={'text': data['text']}
        )
        return question

    @staticmethod
    def __cleanup_questions(survey_id, questions_data):

        existing_questions = []
        for item in questions_data:
            for question_type, value in item.items():
                order_value = value.get('order')
                existing_questions.append((order_value, question_type))
                break
        existing_questions_set = set(existing_questions)


        # Use annotate to ensure all queries return the same structure
        current_questions = (
            MatrixQuestion.objects.filter(survey_id=survey_id)
            .values('order').annotate(question_category=Value('MatrixQuestion'))
            .union(
                MultipleChoiceQuestion.objects.filter(survey_id=survey_id)
                .values('order').annotate(question_category=Value('MultipleChoiceQuestion')),
                RankingQuestion.objects.filter(survey_id=survey_id)
                .values('order').annotate(question_category=Value('RankingQuestion')),
                YesNoQuestion.objects.filter(survey_id=survey_id)
                .values('order').annotate(question_category=Value('YesNoQuestion'))
            )
        )

        current_questions_set = set((q['order'], q['question_category']) for q in current_questions)
        # Delete questions that are no longer in the request
        for order, question_type in current_questions_set:
            if (order, question_type) not in existing_questions_set:
                if question_type == "MatrixQuestion":
                    MatrixQuestion.objects.filter(survey_id=survey_id, order=order).delete()
                elif question_type == "MultipleChoiceQuestion":
                    MultipleChoiceQuestion.objects.filter(survey_id=survey_id, order=order).delete()
                elif question_type == "RankingQuestion":
                    RankingQuestion.objects.filter(survey_id=survey_id, order=order).delete()
                elif question_type == "YesNoQuestion":
                    YesNoQuestion.objects.filter(survey_id=survey_id, order=order).delete()