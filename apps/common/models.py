from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class TestGroup(models.Model):
    """Model for tests"""

    title = models.CharField(verbose_name='Название теста', max_length=255)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('test_detail', kwargs={'pk': self.pk})


class Question(models.Model):
    """Model for questions for test"""

    text = models.TextField(verbose_name='Вопрос')
    number = models.IntegerField(
        verbose_name='Номер вопроса', blank=True, null=True
    )
    test = models.ForeignKey(
        to=TestGroup, verbose_name='Тест', related_name='test_questions',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.number is None:
            count = Question.objects.filter(test=self.test).count()
            self.number = count + 1 if count > 0 else 1
        super(Question, self).save(force_insert, force_update, using, update_fields)


class AnswerToQuestion(models.Model):
    """Model for answer to the questions"""

    text = models.TextField(verbose_name='Вопрос')
    question = models.ForeignKey(
        to=Question, verbose_name='Вопрос',
        related_name='question_answers', on_delete=models.CASCADE
    )
    is_right = models.BooleanField(verbose_name='Правильный ответ', default=False)
    user = models.ManyToManyField(
        to=User, verbose_name='Пользователь', related_name='user_answer',
        blank=True
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.text
