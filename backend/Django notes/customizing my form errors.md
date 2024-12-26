

```python
from django import forms

class CustomUserForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        required=True,
        error_messages={
            'required': 'Please enter your username.',
            'max_length': 'Username cannot be longer than 30 characters.',
            'invalid': 'Please enter a valid username.',
        }
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'Email address is required.',
            'invalid': 'Enter a valid email address.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        error_messages={
            'required': 'Password is required.',
            'invalid': 'Enter a valid password.',
        }
    )
    confirm_password/password2 = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        error_messages={
            'required': 'Please confirm your password.',
            'invalid': 'Enter a valid confirmation password.',
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('Passwords do not match. Please try again.')

```