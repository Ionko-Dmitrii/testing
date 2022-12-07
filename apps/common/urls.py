from django.urls import path

from apps.common.views import TestDetailView, AddedAnswerView

urlpatterns = [
    path('test/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
    path('add-answer', AddedAnswerView.as_view(), name='add_answer')
]
