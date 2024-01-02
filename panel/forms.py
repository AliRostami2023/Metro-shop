from django import forms
from django.core.exceptions import ValidationError

from account.models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'last name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'username'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

        error_messages = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'avatar': '',
        }

        labels = {
            'first_name': 'first name',
            'last_name': 'last name',
            'username': 'user name',
            'avatar': 'avatar',
        }


class ChangePasswordUserForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'current password', 'class': 'form-control'}),
        label=''
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'new password', 'class': 'form-control'}),
        label=''
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'confirm new password', 'class': 'form-control'}),
        label=''
    )

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if new_password == confirm_password:
            return confirm_password

        raise ValidationError('new password and confirm password must match!!!')

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')

        if len(new_password) >= 8:
            return new_password

        raise ValidationError('password have to have 8 number or char!!!')
