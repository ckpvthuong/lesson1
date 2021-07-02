from rest_framework import generics

# Create your views here.
from rest_framework.response import Response

from module.survey.models import Survey
from module.survey.serializers import SurveyListSerializer


class SurveyListView(generics.ListCreateAPIView):
    serializer_class = SurveyListSerializer

    def get_queryset(self):
        return Survey.objects \
            .prefetch_related('questions') \
            .prefetch_related('questions__answer').filter()

