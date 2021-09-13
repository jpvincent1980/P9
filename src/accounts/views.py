from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView

from accounts.forms import SignupForm, LoginForm
from accounts.models import CustomUser, UserFollows


# Create your views here.
class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = "../account-created/"

    def form_valid(self, form):
        # Override form_valid function from parent class to add automatic login
        # after signup
        form.save()
        username = self.request.POST["username"]
        password = self.request.POST["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(reverse('accounts:index'))


def index_view(request):
    form = LoginForm
    context = {"form": form}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("accounts:index")
    return render(request, "accounts/index.html", context)


def account_created_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
    return render(request, "accounts/account-created.html", context)


def logout_view(request):
    logout(request)
    return redirect("accounts:index")


def subscriptions_view(request):
    current_user_id = request.user.id
    followers = UserFollows.objects.filter(followed_user_id=current_user_id).values()
    followers = [follower["user_id"] for follower in followers]
    followed_users = UserFollows.objects.filter(user_id=current_user_id).values()
    followed_users = [user["followed_user_id"] for user in followed_users]
    followers = [CustomUser.objects.get(pk=follower_id) for follower_id in followers]
    followed_users = [CustomUser.objects.get(pk=user_id) for user_id in followed_users]
    context = {"followers": followers,
               "followed_users": followed_users}
    if request.method == "POST":
        if request.POST["user_search"]:
            searched_user = CustomUser.objects.filter(username__icontains=request.POST["user_search"])
            current_subscriptions = UserFollows.objects.filter(user_id=current_user_id).values()
            user_ids_to_exclude = [i["followed_user_id"] for i in current_subscriptions]
            # Exclude already followed users
            for id in user_ids_to_exclude:
                searched_user = searched_user.exclude(id=id)
            if request.POST["user_search"] != "" and searched_user.count() > 0:
                context = {"followers": followers,
                           "followed_users": followed_users,
                           "result": searched_user,
                           "result_type": "QuerySet"}
            else:
                message = "Aucun utilisateur auquel vous n'êtes pas déjà " \
                          "abonné n'a été trouvé."
                context = {"followers": followers,
                           "followed_users": followed_users,
                           "result": [message],
                           "result_type": "str"}
    return render(request, "accounts/subscriptions.html", context)


def subscribe_view(request, user_id):
    subscription = UserFollows.objects.create(followed_user_id=user_id, user_id=request.user.id)
    subscription.save()
    return redirect("accounts:subscriptions")
    # return subscriptions_view(request)


def unsubscribe_view(request, user_id):
    subscription = UserFollows.objects.filter(followed_user_id=user_id, user_id=request.user.id)
    subscription.delete()
    return subscriptions_view(request)
