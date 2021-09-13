from itertools import chain
from operator import attrgetter

from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView

from reviews.forms import ReviewForm, TicketForm


# Create your views here.
from reviews.models import Ticket, Review


def create_review_view(request, ticket_id=None):
    form = ReviewForm()
    context = {"form": form,
               "ticket_id": ticket_id}
    return render(request, "reviews/review.html", context)


class UpdateReviewView(UpdateView):
    pass


class CreateTicketView(CreateView):
    form_class = TicketForm
    template_name = "reviews/ticket.html"


class UpdateTicketView(UpdateView):
    form_class = TicketForm
    template_name = "reviews/ticket.html"


class DeleteTicketView(DeleteView):
    form_class = TicketForm
    template_name = "reviews/ticket.html"


def posts_view(request):
    tickets = Ticket.objects.filter(user=request.user.id)
    reviews = Review.objects.filter(user=request.user.id)
    posts = sorted(chain(tickets, reviews), key=attrgetter("time_created"), reverse=True)
    context = {"posts": posts}
    return render(request, "reviews/posts.html", context)
