from itertools import chain
from operator import attrgetter

from django.db.models import Value, CharField
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from accounts.models import CustomUser
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
                   "ticket": ticket,
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
