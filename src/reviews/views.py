from itertools import chain
from operator import attrgetter

from django.db.models import Value, CharField, QuerySet
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from accounts.models import CustomUser, UserFollows
from reviews.forms import ReviewForm, TicketForm, UpdateTicketForm, \
    UpdateReviewForm
from reviews.models import Ticket, Review


# Create your views here.
class ReviewDetailView(DetailView):
    pass


def create_review_view(request, ticket_id=None):
    review_form = ReviewForm()
    if ticket_id and request.method != "POST":
        ticket = Ticket.objects.get(pk=ticket_id)
        context = {"review_form": review_form,
                   "post": ticket,
                   "ticket_id": ticket_id}
        return render(request, "reviews/review.html", context)
    if request.method == "POST":
        ticket = Ticket.objects.get(pk=ticket_id)
        review = Review.objects.create(headline=request.POST.get("headline"),
                                       rating=request.POST.get("rating"),
                                       body=request.POST.get("body"),
                                       user=request.user,
                                       ticket=ticket)
        return redirect("reviews:posts")
    ticket_form = TicketForm()
    context = {"review_form": review_form,
               "ticket_form": ticket_form}
    return render(request, "reviews/review.html", context)


class UpdateReviewView(UpdateView):
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


def delete_review_view(request, review_id):
    review = Review.objects.get(id=review_id)
    review.delete()
    return posts_view(request)


class TicketDetailView(DetailView):
    template_name = "reviews/posts.html"


class CreateTicketView(CreateView):
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


class UpdateTicketView(UpdateView):
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


def delete_ticket_view(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket.delete()
    return redirect("reviews:posts")


def posts_view(request):
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
    user_tickets = Ticket.objects.filter(user=user_id)
    reviews = Review.objects.values()
    answered_tickets_ids = [element.get("ticket_id") for element in reviews]
    user_open_tickets = user_tickets.exclude(id__in=answered_tickets_ids)
    user_open_tickets = user_open_tickets.annotate(content_type=Value("Open-tickets", CharField()))
    return user_open_tickets


# def get_own_tickets_answered_by_others(user_id):
#     user_tickets = Ticket.objects.filter(user=user_id)
#     reviews = Review.objects.values()
#     answered_by_others = [element.get("ticket_id") for element in reviews if element["user_id"] != user_id]
#     user_tickets_closed_by_others = user_tickets.filter(id__in=answered_by_others)
#     user_tickets_closed_by_others = user_tickets_closed_by_others.annotate(content_type=Value("Closed-tickets", CharField()))
#     return user_tickets_closed_by_others


def get_own_tickets_answered_by_self(user_id):
    user_tickets = Ticket.objects.filter(user=user_id)
    reviews = Review.objects.values()
    answered_by_self = [element.get("ticket_id") for element in reviews if element["user_id"] == user_id]
    user_tickets_closed_by_self = user_tickets.filter(id__in=answered_by_self)
    user_tickets_closed_by_self = user_tickets_closed_by_self.annotate(content_type=Value("Closed-tickets", CharField()))
    return user_tickets_closed_by_self


def get_followed_users_open_tickets(user_id):
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
    others_tickets = Ticket.objects.exclude(user_id=user_id).values()
    others_tickets_ids = [ticket["id"] for ticket in others_tickets]
    reviews = Review.objects.filter(user_id=user_id).filter(ticket_id__in=others_tickets_ids)
    reviews = reviews.annotate(content_type=Value("Review", CharField()))
    return reviews


def get_own_reviews_from_own_tickets(user_id):
    others_tickets = Ticket.objects.exclude(user_id=user_id).values()
    others_tickets_ids = [ticket["id"] for ticket in others_tickets]
    reviews = Review.objects.filter(user_id=user_id).exclude(ticket_id__in=others_tickets_ids)
    reviews = reviews.annotate(content_type=Value("Review", CharField()))
    return reviews


def get_reviews_from_followed_users(user_id):
    followed_users = UserFollows.objects.filter(user_id=user_id).values()
    followed_users_ids = [user["followed_user_id"] for user in followed_users]
    followed_users_reviews = Review.objects.none()
    for followed_user in followed_users_ids:
        user_review = Review.objects.filter(user_id=followed_user)
        user_review = user_review.annotate(content_type=Value("Review", CharField()))
        followed_users_reviews = followed_users_reviews.union(user_review)
    return followed_users_reviews
