from django.contrib import admin

from apps.common.forms import QuestionFormAdmin
from apps.common.models import TestGroup, Question, AnswerToQuestion


@admin.register(TestGroup)
class TestGroupAdmin(admin.ModelAdmin):
    pass


class AnswerToQuestionInline(admin.StackedInline):
    model = AnswerToQuestion
    extra = 2
    fields = ('text', 'is_right')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerToQuestionInline,)
    list_display = ('test', 'text', 'number')
    form = QuestionFormAdmin
    fields = ('test', 'text')
