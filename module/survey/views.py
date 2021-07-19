import json
import logging
import time
from datetime import timedelta

from django.conf import settings
from django.core.cache import cache
from rest_framework import generics, status, HTTP_HEADER_ENCODING
# Create your views here.
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from common.errors import ErrCannotCreateEntity
from module.survey.backends import CustomJWTAuthentication
from module.survey.models import Survey, Question
from module.survey.serializers import SurveyListSerializer, SurveyCreateSerializer, SurveyUpdateSerializer, \
    QuestionSerializer

logger = logging.getLogger(__name__)


class SurveyListView(generics.ListCreateAPIView):
    serializer_class = SurveyListSerializer

    def get_queryset(self):
        return Survey.objects \
            .prefetch_related('questions') \
            .prefetch_related('questions__answer').filter()

    def create(self, request, *args, **kwargs):
        try:
            self.serializer_class = SurveyCreateSerializer
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            raise ErrCannotCreateEntity(entity='Survey', err=e)


class SurveyGetView(generics.UpdateAPIView):
    serializer_class = SurveyUpdateSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Survey.objects.get(id=pk)
        return queryset

    def get_object(self):
        obj = self.get_queryset()
        return obj


class ListQuestionView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        Question.objects.get()
        return Question.objects.all()


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        new_token_dict = {
            "user_agent": request.META["HTTP_USER_AGENT"],
            "access": serializer.validated_data["access"],
            "refresh": serializer.validated_data["refresh"],
        }

        user = serializer.user
        expire = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] or timedelta(minutes=30)
        key = f'user_{user.id}_token_{time.time()}'
        value = json.dumps(new_token_dict)
        cache.set(key, value, expire.total_seconds())

        logger.debug(f'redis: saved: {key}={value}')

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(generics.DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        access_token = request.META.get(api_settings.AUTH_HEADER_NAME).split()[1]

        key_pattern = f'user_{request.user.id}_token_*'
        keys = cache.keys(key_pattern)
        dict = cache.get_many(keys)

        target_key = None
        for k in dict:
            token_dict = json.loads(dict[k])
            if token_dict["access"] == access_token:
                target_key = k
                break

        cache.delete(target_key)
        logger.debug(f'redis: deleted: {target_key}')

        return Response(status=status.HTTP_204_NO_CONTENT)


class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        validated_token = CustomJWTAuthentication().get_validated_token(
            serializer.validated_data["access"].encode(HTTP_HEADER_ENCODING))
        user = CustomJWTAuthentication().get_user(validated_token)

        new_token_dict = {
            "user_agent": request.META["HTTP_USER_AGENT"],
            "access": serializer.validated_data["access"],
            "refresh": request.data["refresh"],
        }
        expire = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] or timedelta(minutes=30)
        key = f'user_{user.id}_token_{time.time()}'
        value = json.dumps(new_token_dict)
        cache.set(key, value, expire.total_seconds())

        logger.debug(f'redis: saved: {key}={value}')
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
