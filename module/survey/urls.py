from django.urls import path

from .views import SurveyListView

urlpatterns = [
    # url(r'', UsersView.as_view(), name='list-user'),
    path('surveys', SurveyListView.as_view(), name='list_survey'),
]
