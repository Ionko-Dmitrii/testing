from django.db.models import Q, Count
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView

from apps.common.forms import AddedAnswerForm
from apps.common.models import TestGroup, Question, AnswerToQuestion


class TestListView(ListView):
    """Endpoint por test list"""

    template_name = 'pages/test-list.html'
    context_object_name = 'test_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = TestGroup.objects.all().annotate(
                count_questions=Count('test_questions', distinct=True),
                count_completed_questions=Count(
                    'test_questions',
                    filter=Q(test_questions__question_answers__user=self.request.user)
                )
            )
        else:
            queryset = []

        return queryset

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(TestListView, self).get_context_data(*args, **kwargs)

        return context


class TestDetailView(DetailView):
    """Endpoint por test detail"""

    template_name = 'pages/test-detail.html'
    model = TestGroup
    context_object_name = 'test_object'

    def get_context_data(self, **kwargs):
        context = super(TestDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            question = Question.objects.filter(
                test_id=self.kwargs.get('pk')).exclude(
                question_answers__user=self.request.user
            ).prefetch_related('question_answers').order_by('number').first()
            context['question'] = question
            if question:
                finish_test = None
            else:
                finish_test = AnswerToQuestion.objects.filter(
                    question__test_id=self.kwargs.get('pk')
                ).aggregate(
                    correct_answers=Count('id', filter=Q(user=self.request.user, is_right=True)),
                    incorrect_answers=Count('id', filter=Q(user=self.request.user, is_right=False)),
                    percentage_correct_answers=(
                            100 / Count('id', filter=Q(user=self.request.user)) *
                            Count('id', filter=Q(user=self.request.user, is_right=True))
                    ),
                )
            context['finish_test'] = finish_test
            context['count_questions'] = Question.objects.filter(
                test_id=self.kwargs.get('pk')).count()

        return context


class AddedAnswerView(View):
    """Endpoint por added answer"""

    def post(self, request, *args, **kwargs):
        form = AddedAnswerForm(data=request.POST, request=request)
        if form.is_valid():
            answer = form.cleaned_data.get('answer')
            answer.user.add(request.user)
            return JsonResponse(dict(message='OK'), status=200)

        return JsonResponse(dict(form.errors), status=400)


@receiver(post_delete, sender=Question)
def added_number_after_delete(sender, instance, **kwargs):
    questions = Question.objects.filter(test=instance.test).order_by('number')
    question_list = []
    for i in range(questions.count()):
        question = questions[i]
        question.number = i + 1
        question_list.append(question)

    Question.objects.bulk_update(question_list, ['number'])
