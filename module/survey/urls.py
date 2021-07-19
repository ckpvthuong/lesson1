from django.conf.urls import url
from django.urls import path, include

from .views import SurveyListView, SurveyGetView, ListQuestionView, LoginView, LogoutView, RefreshTokenView

urlpatterns = [
    # url(r'', UsersView.as_view(), name='list-user'),
    path('surveys/', SurveyListView.as_view(), name='list_survey'),
    path('survey/<int:pk>/', SurveyGetView.as_view(), name='get_survey'),
    path('questions/', ListQuestionView.as_view(), name='list_question'),
    url(r'', include('djoser.urls')),
    url(r'', include('djoser.urls.jwt')),
    url(r'login/', LoginView.as_view(), name='login'),
    url(r'logout/', LogoutView.as_view(), name='logout'),
    url(r'refresh-token/', RefreshTokenView.as_view(), name='refresh-token')
]
