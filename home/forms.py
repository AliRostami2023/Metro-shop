from django import forms

from home.models import ContactUs


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'mobile', 'email', 'subject', 'body']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'full name',
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'phone number',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'subject',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'body',
            }),
        }

        labels = {
            'full_name': '',
            'mobile': '',
            'email': '',
            'subject': '',
            'body': '',
        }


