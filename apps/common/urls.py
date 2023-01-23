from django.urls import path

from apps.common.views import TestDetailView, AddedAnswerView, RightAnswerView

urlpatterns = [
    path('test/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
    path('add-answer', AddedAnswerView.as_view(), name='add_answer'),
    path('right_answer/', RightAnswerView.as_view(), name='right_answer')
]
