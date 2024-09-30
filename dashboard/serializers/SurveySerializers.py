from rest_framework import serializers

from dashboard.models.Survey import Survey


class CreateSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'is_published', 'created_at']
        read_only_fields = ['is_published', 'expires_at']

class PublishSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['is_published', 'expires_at']
        extra_kwargs = {
            'is_published': {'required': True},
            'expires_at': {'required': True},
        }