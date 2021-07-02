from django.contrib import admin
from module.survey.models import Survey, Question, Answer


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'updated')
    list_filter = ('id', 'name', 'created', 'updated')
    search_fields = ('id', 'name')


admin.site.register(Survey, SurveyAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'updated')
    list_filter = ('id', 'name', 'created', 'updated')
    search_fields = ('id', 'name')


admin.site.register(Question, QuestionAdmin)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'question', 'created', 'updated')
    list_filter = ('id', 'name', 'created', 'updated')
    search_fields = ('id', 'name')
