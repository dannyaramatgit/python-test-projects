from .models import Question, Choice
from rest_framework import serializers

class ChoiceSerializer(serializers.ModelSerializer):
    # question = serializers.ReadOnlyField(source='question.question_text')

    class Meta:
        model = Choice
        fields = ['id','choice_text','question', 'votes']


class QuestionSerializer(serializers.ModelSerializer):
    choices = serializers.HyperlinkedRelatedField(many=True, view_name='choice', read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'choices']


