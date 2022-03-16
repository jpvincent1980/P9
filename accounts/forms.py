from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, forms
from accounts.models import CustomUser


class SignupForm(UserCreationForm):
    """
    A form inheriting from UserCreationForm to create a CustomUser instance.
    """
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["username"].help_text = None
        self.fields["password1"].help_text = "<ul>" \
                                             "<li>Votre mot de passe doit " \
                                             "contenir au minimum 8 caractères.</li>" \
                                             "<li>Votre mot de passe ne peut " \
                                             "pas être entièrement numérique.</li>" \
                                             "</ul>"
        self.fields["password2"].help_text = None

    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2"]
        widgets = {"username": forms.fields.TextInput(attrs={"placeholder": "Pseudo"})}


class LoginForm(AuthenticationForm):
    """
    A form inheriting from AuthenticationForm for users to login.
    """
    pass
