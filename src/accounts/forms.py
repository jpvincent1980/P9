from django.forms import forms, ModelForm
from accounts.models import CustomUser


class SignupForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password"]
        help_texts = {"username": None}