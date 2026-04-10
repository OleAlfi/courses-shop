from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import Review


class PaymentForm(forms.Form):
    amount = forms.DecimalField(label="Payment amount", max_digits=10, decimal_places=2)
    card_number = forms.CharField(
        label="Card number",
        max_length=16,
        min_length=16,
        validators=[RegexValidator(r'^\d{16}$', 'Enter a valid 16-digit card number.')]
    )
    expiry_month = forms.IntegerField(
        label="Expiry MM:",
        min_value=1,
        max_value=12
    )
    expiry_year = forms.IntegerField(
        label="Expiry YY:",
        min_value=26,
        max_value=99
    )
    cvv = forms.IntegerField(
        label="CVV",
        min_value=100,
        max_value=999
    )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
        ]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your comment...'}),
        }
