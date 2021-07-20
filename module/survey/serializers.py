from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from module.survey.models import Survey, Question, Answer

User = get_user_model()


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class SurveyListSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ['id', 'name', 'questions']


class SurveyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'name', 'created']
        extra_kwargs = {
            'name': {'required': False, 'allow_null': True}
        }

    # def validate(self, attrs):
    #     return attrs

    def validate_name(self, name):
        try:
            Survey.objects.get(name=name)
            raise ValidationError(detail="Name đã tồn tại", code="name_existed")
        except Survey.DoesNotExist:
            return name
        except Survey.MultipleObjectsReturned:
            raise ValidationError(detail="Name đã tồn tại", code="name_existed")
        except Exception as e:
            raise e


class SurveyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'name', 'created']
        extra_kwargs = {
            'name': {'required': False, 'allow_null': True}
        }


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        #fields = ['username', 'id', 'email', 'password']
        extra_kwargs = {'email': {'required': True, 'allow_null': True}}
