from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from account.forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from account.models import User


# Create your views here.


class RegisterView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('login-page'))
        return super().dispatch(*args, **kwargs)

    def get(self, request: HttpRequest):
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request: HttpRequest):
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            user_name = form.cleaned_data.get('user_name')
            user_email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()

            if user:
                form.add_error('email', 'There is an email entered...')
            else:
                new_user = User(email=user_email, username=user_name, email_active_code=get_random_string(72),
                                first_name=name, is_active=False)
                new_user.set_password(password)
                new_user.save()
                # send email
                messages.success(request, 'check email for active your account.')

        return render(request, 'account/register.html', {'form': form})


class ActivateAccount(View):
    def get(self, request: HttpRequest, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                # todo:show message success to user
                return redirect(reverse('login-page'))
            else:
                # todo:show message activate account
                pass

        raise Http404


class LoginView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('login-page'))
        return super().dispatch(*args, **kwargs)

    def get(self, request: HttpRequest):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request: HttpRequest):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('password')
            user: User = User.objects.filter(username__iexact=user_name).first()
            if user:
                if not user.is_active:
                    form.add_error('email', 'your account is not active !!!')

                else:
                    is_password_currect = user.check_password(password)
                    if is_password_currect:
                        login(request, user)
                        return redirect(reverse('home-page'))
                    else:
                        form.add_error('password', 'The password is wrong !!!')

            else:
                form.add_error('user_name', 'User with this information was not found !!!')

        return render(request, 'account/login.html', {'form': form})


class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        form = ForgetPasswordForm()
        return render(request, 'account/forget-password.html', {'form': form})

    def post(self, request: HttpRequest):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user:
                # send_email('تغییر کلمه عبور', user.email, {'user': user}, 'emails/reset-password.html')
                messages.success(request, 'check email please !')
                return redirect(reverse('change-pass-page'))

        return render(request, 'account/forget-password.html', {'form': form})


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login-page'))

        form = ResetPasswordForm()
        return render(request, 'account/reset-password.html', {'form': form})

    def post(self, request: HttpRequest, active_code):
        form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if form.is_valid():
            if user is None:
                return redirect(reverse('login-page'))
            else:
                new_user_pass = form.cleaned_data.get('password')
                user.set_password(new_user_pass)
                user.email_active_code = get_random_string(72)
                user.is_active = True
                user.save()
                return redirect(reverse('login-page'))

        return render(request, 'account/reset-password.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home-page'))

