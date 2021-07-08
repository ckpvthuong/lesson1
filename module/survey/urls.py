from django.urls import path

from .views import SurveyListView, SurveyGetView

urlpatterns = [
    # url(r'', UsersView.as_view(), name='list-user'),
    path('surveys', SurveyListView.as_view(), name='list_survey'),
    path('survey/<int:pk>', SurveyGetView.as_view(), name='get_survey'),
]
