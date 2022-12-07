from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email', 'password1',
            'password2'
        )


class UserLoginForm(AuthenticationForm):

    error_messages = {
        'username': [_(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        )],
        'inactive': _("This account is inactive."),
    }

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['username'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )
