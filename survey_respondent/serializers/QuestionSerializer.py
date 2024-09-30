from rest_framework import serializers
from survey_studio.models.Questions import MatrixQuestion, MultipleChoiceQuestion, RankingQuestion, YesNoQuestion

class BaseQuestionSerializer(serializers.ModelSerializer):
    question_type = serializers.CharField(source='get_question_type_display')

    class Meta:
        fields = ['text', 'order']

class MatrixQuestionSerializer(BaseQuestionSerializer):
    rows = serializers.JSONField()
    columns = serializers.JSONField()

    class Meta(BaseQuestionSerializer.Meta):
        model = MatrixQuestion
        fields = BaseQuestionSerializer.Meta.fields + ['rows', 'columns']

class MultipleChoiceQuestionSerializer(BaseQuestionSerializer):
    options = serializers.JSONField()

    class Meta(BaseQuestionSerializer.Meta):
        model = MultipleChoiceQuestion
        fields = BaseQuestionSerializer.Meta.fields + ['options']

class RankingQuestionSerializer(BaseQuestionSerializer):
    options = serializers.JSONField()

    class Meta(BaseQuestionSerializer.Meta):
        model = RankingQuestion
        fields = BaseQuestionSerializer.Meta.fields + ['options']

class YesNoQuestionSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta):
        model = YesNoQuestion
        fields = BaseQuestionSerializer.Meta.fields

class QuestionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if isinstance(instance, MatrixQuestion):
            data = MatrixQuestionSerializer(instance).data
            data['question_type'] = 'matrix'
        elif isinstance(instance, MultipleChoiceQuestion):
            data = MultipleChoiceQuestionSerializer(instance).data
            data['question_type'] = 'multiple_choice'
        elif isinstance(instance, RankingQuestion):
            data = RankingQuestionSerializer(instance).data
            data['question_type'] = 'ranking'
        elif isinstance(instance, YesNoQuestion):
            data = YesNoQuestionSerializer(instance).data
            data['question_type'] = 'yes_no'
        else:
            data = super().to_representation(instance)

        return data
