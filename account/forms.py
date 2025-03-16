from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'name'}), label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}), label='')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm password'}), label='')
    captcha = CaptchaField()

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return password
        raise ValidationError('password != confirm password')

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # check username for more than 8 char and num

        if len(password) >= 8:
            return password

        raise ValidationError('password have to more than 8 char or number.')


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}), label='')
    captcha = CaptchaField()


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email'}), label='')


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'new password'}), label='')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm new password'}),
                                       label='')
