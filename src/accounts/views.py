from itertools import chain
from operator import attrgetter

from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Value, CharField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView

from accounts.forms import SignupForm, LoginForm
from accounts.models import CustomUser, UserFollows
from reviews.models import Ticket, Review


# Create your views here.
def index_view(request):
    if request.user.is_authenticated:
        followed_users = UserFollows.objects.filter(user_id=request.user.id).values()
        followed_users = [user.get("followed_user_id") for user in followed_users]
        # Tickets des utilisateurs suivis
        followed_users_tickets = Ticket.objects.filter(user_id__in=followed_users).annotate(content_type=Value("Ticket", CharField()))
        # Critiques des utilisateurs suivis
        followed_users_reviews = Review.objects.filter(user_id__in=followed_users).annotate(content_type=Value("Review", CharField()))
        posts = sorted(chain(followed_users_tickets,followed_users_reviews),
                       key=attrgetter("time_created"),
                       reverse=True)
        context = {"Test": followed_users_tickets,
                   "posts": posts}
        return render(request, "reviews/flux.html", context)
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
    nb_of_followers = followers.aggregate(total_followers=Count("user_id"))
    nb_of_followers = nb_of_followers.get("total_followers")
    followers = [follower["user_id"] for follower in followers]
    followed_users = UserFollows.objects.filter(user_id=current_user_id).values()
    nb_of_subscriptions = followed_users.aggregate(total_subscriptions=Count("followed_user_id"))
    nb_of_subscriptions = nb_of_subscriptions.get("total_subscriptions")
    followed_users = [user["followed_user_id"] for user in followed_users]
    followers = [CustomUser.objects.get(pk=follower_id) for follower_id in followers]
    followed_users = [CustomUser.objects.get(pk=user_id) for user_id in followed_users]
    context = {"nb_of_followers": nb_of_followers,
               "nb_of_subscriptions": nb_of_subscriptions,
               "followers": followers,
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
                context = {"nb_of_followers": nb_of_followers,
                           "nb_of_subscriptions": nb_of_subscriptions,
                           "followers": followers,
                           "followed_users": followed_users,
                           "result": searched_user,
                           "result_type": "QuerySet"}
            else:
                message = "Aucun utilisateur auquel vous n'êtes pas déjà " \
                          "abonné n'a été trouvé."
                context = {"nb_of_followers": nb_of_followers,
                           "nb_of_subscriptions": nb_of_subscriptions,"followers": followers,
                           "followed_users": followed_users,
                           "result": [message],
                           "result_type": "str"}
    return render(request, "accounts/subscriptions.html", context)


def subscribe_view(request, user_id):
    subscription = UserFollows.objects.create(followed_user_id=user_id, user_id=request.user.id)
    subscription.save()
    return redirect("accounts:subscriptions")


def unsubscribe_view(request, user_id):
    subscription = UserFollows.objects.filter(followed_user_id=user_id, user_id=request.user.id)
    subscription.delete()
    return subscriptions_view(request)
