from rest_framework import serializers
from .models import Question, Choice


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(required=True, allow_blank=False, max_length=100)
    pub_date = serializers.DateTimeField(required=True)

    def create(self, validated_data):
        return Question.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.question_text = validated_data.get('question_text', instance.title)
        instance.pub_date = validated_data.get('pub_date', instance.code)
        instance.save()
        return instance