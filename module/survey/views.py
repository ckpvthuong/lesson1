from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser

from common.permissions import IsOwnerOrReadOnly
from module.survey.models import Survey, Answer, Question
from module.survey.serializers import SurveyListSerializer, QuestionSerializer, AnswerSerializer


# Create your views here.


class SurveyListView(generics.ListCreateAPIView):
    serializer_class = SurveyListSerializer
    permission_classes = [IsAdminUser | IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created', 'updated']
    ordering = ['created']
    search_fields = ['name']

    def get_queryset(self):
        return Survey.objects \
            .prefetch_related('questions') \
            .prefetch_related('questions__answer')


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAdminUser | IsOwnerOrReadOnly]
    ordering_fields = ['created', 'updated']
    ordering = ['created']
    search_fields = ['name']
    filterset_fields = ['survey_id']

    def get_queryset(self):
        return Question.objects \
            .prefetch_related('answer')


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAdminUser | IsOwnerOrReadOnly]
    ordering_fields = ['created', 'updated']
    ordering = ['created']
    search_fields = ['name']
    filterset_fields = ['question_id']
