from itertools import chain
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, CharField
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView

from accounts.models import CustomUser, UserFollows
from reviews.forms import ReviewForm, TicketForm, UpdateTicketForm, \
    UpdateReviewForm
from reviews.models import Ticket, Review


# Create your views here.
@login_required
def create_review_view(request, ticket_id=None):
    """
    A function-based view to create a new review in response to a ticket.

    Context:
        ticket_form: An instance of :form:"review.TicketForm"
        ticket_id: Ticket id number if the review is in response of a ticket
        post: An instance of :model:"reviews.Ticket"
        review_form: An instance of :form:"reviews.ReviewForm"

    Template:
        :template:"reviews/review.html"
    """
    review_form = ReviewForm()
    if ticket_id and request.method != "POST":
        ticket = Ticket.objects.get(pk=ticket_id)
        context = {"review_form": review_form,
                   "post": ticket,
                   "ticket_id": ticket_id}
        return render(request, "reviews/review.html", context)
    if ticket_id and request.method == "POST":
        ticket = Ticket.objects.get(pk=ticket_id)
        Review.objects.create(headline=request.POST.get("headline"),
                                       rating=request.POST.get("rating"),
                                       body=request.POST.get("body"),
                                       user=request.user,
                                       ticket=ticket)
        return redirect("reviews:posts")
    if request.method == "POST":
        ticket = Ticket.objects.create(title=request.POST.get("title"),
                                       description=request.POST.get("description"),
                                       image=request.FILES.get("image"),
                                       user=request.user)
        Review.objects.create(headline=request.POST.get("headline"),
                                       rating=request.POST.get("rating"),
                                       body=request.POST.get("body"),
                                       user=request.user,
                                       ticket=ticket)
        return redirect("reviews:posts")
    ticket_form = TicketForm()
    context = {"review_form": review_form,
               "ticket_form": ticket_form}
    return render(request, "reviews/review.html", context)


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    """
    A class-based view to update an instance of Review model

    Context:
        :form:"reviews.UpdateReviewForm"

    Template:
        :template:"reviews/review.html"
    """
    login_url = "accounts:index"
    model = Review
    form_class = UpdateReviewForm
    template_name = "reviews/review.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateReviewView, self).get_context_data(**kwargs)
        context["review_form"] = context["form"]
        return context

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user = CustomUser.objects.get(pk=self.request.user.id)
        ticket.save()
        return redirect("reviews:posts")


@login_required
def delete_review_view(request, pk):
    """
    A function-based view to delete an instance of Review model

    Context:
        None

    Template:
        None
    """
    review = Review.objects.get(id=pk)
    review.delete()
    return posts_view(request)


class CreateTicketView(LoginRequiredMixin, CreateView):
    """
    A class-based view to create an instance of Ticket model

    Context:
        :form:"reviews.TicketForm"

    Template:
        :template:"reviews/ticket.html"
    """
    form_class = TicketForm
    template_name = "reviews/ticket.html"

    def get_context_data(self, **kwargs):
        context = super(CreateTicketView, self).get_context_data(**kwargs)
        context["ticket_form"] = context["form"]
        return context

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user = CustomUser.objects.get(pk=self.request.user.id)
        ticket.save()
        return redirect("reviews:posts")


class UpdateTicketView(LoginRequiredMixin, UpdateView):
    """
    A class-based view to update an instance of Ticket model

    Context:
        :form:"reviews.UpdateTicketForm"

    Template:
        :template:"reviews/ticket.html"
    """
    model = Ticket
    form_class = UpdateTicketForm
    template_name = "reviews/ticket.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateTicketView, self).get_context_data(**kwargs)
        context["ticket_form"] = context["form"]
        return context

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user = CustomUser.objects.get(pk=self.request.user.id)
        ticket.save()
        return redirect("reviews:posts")


@login_required
def delete_ticket_view(request, pk):
    """
    A function-based view to delete an instance of Ticket model

    Context:
        None

    Template:
        None
    """
    ticket = Ticket.objects.get(id=pk)
    ticket.delete()
    return redirect("reviews:posts")


@login_required
def posts_view(request):
    """
    A function-based view to display instances of Tickets and Reviews created
     by user

    Context:
        posts: :model:"reviews.Ticket"
               :model:"reviews.Review"

    Template:
        :template:"reviews/posts.html"
    """
    tickets = Ticket.objects.filter(user=request.user.id)
    tickets = tickets.annotate(content_type=Value("Ticket", CharField()))
    reviews = Review.objects.filter(user=request.user.id)
    reviews = reviews.annotate(content_type=Value("Review", CharField()))
    posts = sorted(chain(tickets, reviews),
                   key=attrgetter("time_created"),
                   reverse=True)
    context = {"posts": posts}
    return render(request, "reviews/posts.html", context)


def get_open_tickets(user_id):
    """
    A function that returns a QuerySet made of user's open tickets.

    Args:
        user_id: user id number

    Returns:
        A QuerySet of user's open tickets
    """
    user_tickets = Ticket.objects.filter(user=user_id)
    reviews = Review.objects.values()
    answered_tickets_ids = [element.get("ticket_id") for element in reviews]
    user_open_tickets = user_tickets.exclude(id__in=answered_tickets_ids)
    user_open_tickets = user_open_tickets.annotate(content_type=Value("Open-tickets", CharField()))
    return user_open_tickets


def get_followed_users_open_tickets(user_id):
    """
    A function that returns a QuerySet made of followed user's open tickets.

    Args:
        user_id: user id number

    Returns:
        A QuerySet of followed user's open tickets
    """
    followed_users = UserFollows.objects.filter(user_id=user_id)
    followed_users = followed_users.values()
    followed_users_ids = [user["followed_user_id"] for user in followed_users]
    followed_users_open_tickets = Ticket.objects.none()
    for user_id in followed_users_ids:
        tickets = get_open_tickets(user_id)
        if tickets.count() != 0:
            followed_users_open_tickets = followed_users_open_tickets.union(tickets)
    return followed_users_open_tickets


def get_followed_users_tickets_answered_by_others(user_id):
    """
    A function that returns a QuerySet made of followed user's tickets answered
    by other users.

    Args:
        user_id: user id number

    Returns:
        A QuerySet of followed user's tickets answered by other users
    """
    followed_users = UserFollows.objects.filter(user_id=user_id).values()
    followed_users_ids = [user["followed_user_id"] for user in followed_users]
    followed_users_tickets = Ticket.objects.none()
    for followed_user in followed_users_ids:
        user_tickets = Ticket.objects.filter(user_id=followed_user).annotate(content_type=Value("Closed-ticket", CharField()))
        followed_users_tickets = followed_users_tickets.union(user_tickets)
    tickets_reviewed_by_others = Review.objects.exclude(user_id=user_id).values()
    tickets_answered_by_others_ids = [review["ticket_id"] for review in tickets_reviewed_by_others]
    tickets_answered_by_others = Ticket.objects.none()
    for ticket_id in tickets_answered_by_others_ids:
        user_ticket = Ticket.objects.filter(id=ticket_id).annotate(content_type=Value("Closed-ticket", CharField()))
        tickets_answered_by_others = tickets_answered_by_others.union(user_ticket)
    followed_users_tickets_answered_by_others = followed_users_tickets.intersection(tickets_answered_by_others)
    return followed_users_tickets_answered_by_others


def get_own_reviews_from_others_tickets(user_id):
    """
    A function that returns a QuerySet made of user's reviews answering to
    other users' tickets

    Args:
        user_id: user id number

    Returns:
        A QuerySet of user's reviews answering to other users' tickets
    """
    others_tickets = Ticket.objects.exclude(user_id=user_id).values()
    others_tickets_ids = [ticket["id"] for ticket in others_tickets]
    reviews = Review.objects.filter(user_id=user_id).filter(ticket_id__in=others_tickets_ids)
    reviews = reviews.annotate(content_type=Value("Review", CharField()))
    return reviews


def get_reviews_from_followed_users(user_id):
    """
    A function that returns a QuerySet made of followed user's reviews.

    Args:
        user_id: user id number

    Returns:
        A QuerySet of followed user's reviews
    """
    followed_users = UserFollows.objects.filter(user_id=user_id).values()
    followed_users_ids = [user["followed_user_id"] for user in followed_users]
    followed_users_reviews = Review.objects.none()
    for followed_user in followed_users_ids:
        user_review = Review.objects.filter(user_id=followed_user)
        user_review = user_review.annotate(content_type=Value("Review", CharField()))
        followed_users_reviews = followed_users_reviews.union(user_review)
    return followed_users_reviews
