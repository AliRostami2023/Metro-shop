from django import forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'name'}), label='')
    user_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}), label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}), label='')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm password'}), label='')

    def clean_confirm_password(self):
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

    def clean_user_name(self):
        username = self.cleaned_data.get('user_name')

        # check username for more than 8 char and num

        if len(username) < 8:
            raise ValidationError('username have to more than 8 char and number.')

        # check username include char and number

        if not any(char.isdigit() for char in username) or not any(char.isalpha() for char in username):
            raise ValidationError('username have to include char and number.')

        return username


class LoginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}), label='')


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email'}), label='')


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'new password'}), label='')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm new password'}),
                                       label='')
