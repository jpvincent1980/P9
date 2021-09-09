from django.shortcuts import render
from django.views.generic import CreateView
from LITReview import settings


# Create your views here.
class SignupView(CreateView):
    model = settings.AUTH_USER_MODEL
    context_object_name = "user"
    template_name = "accounts/signup.html"
    fields = ["username", "password"]


def index(request):
    context = {}
    return render(request, "index.html", context)
