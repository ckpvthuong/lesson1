from rest_framework import generics, status

# Create your views here.
from rest_framework.response import Response

from common.errors import ErrCannotCreateEntity
from module.survey.models import Survey
from module.survey.serializers import SurveyListSerializer, SurveyCreateSerializer, SurveyUpdateSerializer


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
