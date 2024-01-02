from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'track_code', 'is_paid', 'created')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'first name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'last name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'phone',
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'country',
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'state',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'city',
            }),
            'zip_code': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'zip code',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'address',
            }),
        }

        labels = {
            'first_name': 'first name',
            'last_name': 'last name',
            'email': 'email',
            'phone_number': 'phone number',
            'country': 'country',
            'state': 'state',
            'city': 'city',
            'zip_code': 'zip code',
            'address': 'address',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone:
            try:
                int(phone)
            except:
                raise forms.ValidationError('Please enter valid phone number !!')
        return phone
