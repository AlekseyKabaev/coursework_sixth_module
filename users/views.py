import secrets

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import User
from users.forms import UserRegisterForm, UserProfileForm

from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейти по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class NewPasswordView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'users/new_password.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = get_object_or_404(User, email=email)

        new_password = get_random_string(length=8)
        hashed_password = make_password(new_password)
        user.password = hashed_password
        user.save()
        send_mail(
            subject="Ваш новый пароль",
            message=f"'Ваш новый пароль для входа в аккаунт: {new_password}'",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return redirect('users:login')


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('mailing:base')

    def get_object(self, queryset=None):
        return self.request.user
