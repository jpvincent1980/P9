from django.shortcuts import render
from django.views.generic import CreateView, FormView
from accounts.forms import SignupForm
from LITReview import settings


# Create your views here.
class SignupView(FormView):
    form_class = SignupForm
    context_object_name = "user"
    template_name = "accounts/signup.html"
    fields = ["username", "password"]
    success_url = "../account-created/"

    # def form_valid(self, form):
    #     return super().form_valid(form)


def index(request):
    form = SignupForm
    context = {"form": form}
    return render(request, "accounts/index.html", context)


def account_created(request):
    context = {}
    return render(request, "accounts/account-created.html", context)
