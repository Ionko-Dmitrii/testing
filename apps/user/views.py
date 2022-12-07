from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.views.generic import CreateView

from apps.user.forms import RegistrationForm, UserLoginForm


class RegistrationView(CreateView):
    """Endpoint for registration user"""

    template_name = 'pages/registration.html'
    form_class = RegistrationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return JsonResponse(
                dict(message='Пользователь зарегистрирован!'), status=200
            )

        return JsonResponse(
            dict(message='Ошибка!', data=form.errors), status=400
        )


class LogInView(LoginView):
    """Endpoint for login user"""
    template_name = 'pages/login.html'
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST)
        if form.is_valid():
            login(request, form.user_cache)

            return JsonResponse(
                dict(message='Пользователь авторизован!'), status=200
            )

        return JsonResponse(
            dict(message='Ошибка!', data=form.error_messages), status=400
        )


class LogoutUserView(LogoutView):
    """Endpoint for logout user"""

    template_name = 'header.html'
    next_page = '/registration/'
