from rest_framework import serializers
from survey_respondent.models.Answers import (
    YesNoAnswer,
    MultipleChoiceAnswer,
    RankingAnswer,
    MatrixAnswer
)

class YesNoAnswerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='respondent.user_id')
    question_text = serializers.CharField(source='question.text')

    class Meta:
        model = YesNoAnswer
        fields = ['user_id', 'question_text', 'answer', 'created_at']

class MultipleChoiceAnswerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='respondent.user_id')
    question_text = serializers.CharField(source='question.text')
    options = serializers.ListField(source='question.options')

    class Meta:
        model = MultipleChoiceAnswer
        fields = ['user_id', 'question_text', 'options', 'selected_option', 'created_at']

class RankingAnswerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='respondent.user_id')
    question_text = serializers.CharField(source='question.text')
    options = serializers.ListField(source='question.options')

    class Meta:
        model = RankingAnswer
        fields = [ 'user_id', 'question_text', 'options', 'ranking', 'created_at']

class MatrixAnswerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='respondent.user_id')
    question_text = serializers.CharField(source='question.text')
    rows = serializers.ListField(source='question.rows')
    columns = serializers.ListField(source='question.columns')

    class Meta:
        model = MatrixAnswer
        fields = ['user_id', 'question_text', 'rows', 'columns', 'answer_matrix', 'created_at']