from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from accounts.forms import SignupForm, LoginForm


# Create your views here.
class SignupView(CreateView):
    form_class = SignupForm
    context_object_name = "user_form"
    template_name = "accounts/signup.html"
    success_url = "../account-created/"


def index_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("accounts:index")
    else:
        form = LoginForm
    context = {"form": form}
    return render(request, "accounts/index.html", context)


def account_created(request):
    context = {}
    return render(request, "accounts/account-created.html", context)


def logout_view(request):
    logout(request)
    return redirect("accounts:index")
