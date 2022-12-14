from django.urls import path

from apps.user.views import RegistrationView, LogInView, LogoutUserView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
