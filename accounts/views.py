from itertools import chain
from operator import attrgetter

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView

from accounts.forms import SignupForm, LoginForm
from accounts.models import CustomUser, UserFollows
from reviews.views import get_followed_users_open_tickets, \
    get_followed_users_tickets_answered_by_others, \
    get_own_reviews_from_others_tickets, get_reviews_from_followed_users


# Create your views here.
def index_view(request):
    """
    A function-based view to display index page

    Context:
        posts: :model:"reviews.Ticket"
               :model:"reviews.Review"
        form:  :form:"accounts.LoginForm"

    Template:
        :template:"accounts/index.html"
    """
    if request.user.is_authenticated:
        # Tickets ouverts des utilisateurs suivis
        open_tickets = get_followed_users_open_tickets(request.user.id)
        # Tickets des utilisateurs suivis répondus par un autre
        closed_posts = get_followed_users_tickets_answered_by_others(request.user.id)
        tickets = open_tickets.union(closed_posts)
        # Reviews de l'utilisateur
        reviews_by_self = get_own_reviews_from_others_tickets(request.user.id)
        # Reviews des utilisateurs suivis
        reviews_by_followed_users = get_reviews_from_followed_users(request.user.id)
        reviews = reviews_by_self.union(reviews_by_followed_users)
        posts = sorted(chain(tickets, reviews),
                       key=attrgetter("time_created"),
                       reverse=True)
        context = {"posts": posts}
        return render(request, "reviews/flux.html", context)
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("accounts:index")
        else:
            form = LoginForm
            message = "Nom d'utilisateur / mot de passe non valides."
            context = {"form": form,
                       "message": message}
    else:
        form = LoginForm
        context = {"form": form}
    return render(request, "accounts/index.html", context)


def login_view(request):
    """
    A function-based view to display index page

    Context:
        next: next url to redirect user once logged in
        form:  :form:"accounts.LoginForm"
        message: A string displayed to ask user to login

    Template:
        :template:"accounts/index.html"
    """
    next_url = request.GET.get("next")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)
    else:
        form = LoginForm
        context = {"next": next_url,
                   "form": form,
                   "message": "Merci de vous identifier ci-dessous :"}
        return render(request, "accounts/index.html", context)


class SignupView(CreateView):
    """
    A class-based view for a visitor to signup

    Context:
        form:  :form:"accounts.SignupForm"

    Template:
        :template:"accounts/signup.html"
    """
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


@login_required
def account_created_view(request):
    """
    A function-based view to display a confirmation message once user account
    has been created

    Context:
        None

    Template:
        :template:"accounts/account-created.html"
    """
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
    return render(request, "accounts/account-created.html", context)


def logout_view(request):
    """
    A function-based view to logout user

    Context:
        None

    Template:
        None
    """
    logout(request)
    return redirect("accounts:index")


@login_required
def subscriptions_view(request):
    """
    A function-based view to display followed users and other users that follow
    user

    Context:
        "nb_of_followers": an integrer representing the number of followers
        "nb_of_subscriptions": an integrer representing the number of followed
        users
        "followers": a QuerySet of CustomUser instances
        "followed_users": a QuerySet of CustomUser instances
        "result": a QuerySet of CustomUser instances
        "result_type": "QuerySet" or "str" to manage results search

    Template:
        :template:"accounts/subscriptions.html"
    """
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
                           "nb_of_subscriptions": nb_of_subscriptions,
                           "followers": followers,
                           "followed_users": followed_users,
                           "result": [message],
                           "result_type": "str"}
    return render(request, "accounts/subscriptions.html", context)


@login_required
def subscribe_view(request, user_id):
    """
    A function-based view to subscribe to another user

    Context:
        None

    Template:
        None
    """
    subscription = UserFollows.objects.create(followed_user_id=user_id, user_id=request.user.id)
    subscription.save()
    return redirect("accounts:subscriptions")


@login_required
def unsubscribe_view(request, user_id):
    """
    A function-based view to unsubscribe from another user

    Context:
        None

    Template:
        None
    """
    subscription = UserFollows.objects.filter(followed_user_id=user_id, user_id=request.user.id)
    subscription.delete()
    return subscriptions_view(request)
