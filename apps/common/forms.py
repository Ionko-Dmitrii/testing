from django import forms

from apps.common.models import AnswerToQuestion, Question


class AddedAnswerForm(forms.Form):
    """Form for added answer for user"""

    answer_id = forms.IntegerField(required=True)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        answer_id = cleaned_data.get('answer_id')
        answer = AnswerToQuestion.objects.filter(id=answer_id).first()
        if answer is None:
            raise forms.ValidationError({'answer_id': 'Нет такого вопроса!!!'})
        if self.request.user in answer.user.all():
            raise forms.ValidationError({'answer_id': 'Вы уже ответили на этот вопрос!!!'})
        self.cleaned_data['answer'] = answer

        return self.cleaned_data


class QuestionFormAdmin(forms.ModelForm):
    """Form for check error questions admin"""

    class Meta:
        model = Question
        fields = '__all__'

    def clean(self):
        cleaned_data = super(QuestionFormAdmin, self).clean()
        count_answer = int(self.data.get('question_answers-TOTAL_FORMS'))
        is_right = []
        for i in range(count_answer):
            if self.data.get(f'question_answers-{i}-is_right'):
                is_right.append(True)
        if len(is_right) < 1:
            raise forms.ValidationError(
                "Один из ответов должен быть правильным!!"
            )
        if len(is_right) == count_answer:
            raise forms.ValidationError(
                "Все ответы не могут быть правильными!!"
            )

        return cleaned_data
