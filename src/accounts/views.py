from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from accounts.forms import SignupForm, LoginForm
from accounts.models import CustomUser


# Create your views here.
class SignupView(CreateView):
    model = CustomUser
    form_class = SignupForm
    context_object_name = "user_form"
    template_name = "accounts/signup.html"
    success_url = "../account-created/"

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            if request.POST["password"] != request.POST["password_confirm"]:
                return HttpResponse("Ca matche pas ...")
            else:
                return HttpResponse("Ca matche !!!")


def index(request):
    form = LoginForm
    context = {"form": form}
    return render(request, "accounts/index.html", context)


def account_created(request):
    context = {}
    return render(request, "accounts/account-created.html", context)
