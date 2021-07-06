from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SurveyListView, QuestionViewSet, AnswerViewSet

urlpatterns = [
    # url(r'', UsersView.as_view(), name='list-user'),
    path('surveys', SurveyListView.as_view(), name='list_survey'),
]

router = DefaultRouter()

router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answer')

urlpatterns += router.urls
