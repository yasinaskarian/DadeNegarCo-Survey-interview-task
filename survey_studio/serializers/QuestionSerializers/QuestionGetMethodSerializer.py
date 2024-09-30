from rest_framework import serializers
from survey_studio.models.Questions import MatrixQuestion, MultipleChoiceQuestion, RankingQuestion, YesNoQuestion
from dashboard.models.Survey import Survey

class YesNoQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = YesNoQuestion
        fields = ['text', 'order']

class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ['text', 'order', 'options']

class MatrixQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatrixQuestion
        fields = ['text', 'order', 'rows', 'columns']

class RankingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankingQuestion
        fields = ['text', 'order', 'options']

class QuestionGetMethodSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = ['id', 'title', 'questions']

    def get_questions(self, obj):
        questions = []

        # Fetch and categorize questions by type
        yes_no_questions = YesNoQuestion.objects.filter(survey=obj).order_by('order')
        multiple_choice_questions = MultipleChoiceQuestion.objects.filter(survey=obj).order_by('order')
        matrix_questions = MatrixQuestion.objects.filter(survey=obj).order_by('order')
        ranking_questions = RankingQuestion.objects.filter(survey=obj).order_by('order')

        # Append serialized questions to the result
        for question in yes_no_questions:
            questions.append({'YesNoQuestion': YesNoQuestionSerializer(question).data})
        for question in multiple_choice_questions:
            questions.append({'MultipleChoiceQuestion': MultipleChoiceQuestionSerializer(question).data})
        for question in matrix_questions:
            questions.append({'MatrixQuestion': MatrixQuestionSerializer(question).data})
        for question in ranking_questions:
            questions.append({'RankingQuestion': RankingQuestionSerializer(question).data})

        return sorted(questions, key=lambda x: list(x.values())[0]['order'])