from django.urls import path

from reviews.views import UpdateReviewView, CreateTicketView, \
    UpdateTicketView, create_review_view, posts_view, delete_ticket_view, \
    delete_review_view, ReviewDetailView, TicketDetailView

# Création d'un espace de noms
app_name = 'reviews'

urlpatterns = [
    path('reviews/<int:pk>', ReviewDetailView.as_view,
         name="detail-review"),
    path('reviews/create-review/<int:ticket_id>', create_review_view,
         name="create-review-ticket"),
    path('reviews/create-review/', create_review_view,
         name="create-review"),
    path('reviews/update-review/<int:pk>', UpdateReviewView.as_view(),
         name="update-review"),
    path('reviews/delete-review/<int:pk>', delete_review_view,
         name="delete-review"),
    path('tickets/<pk>', TicketDetailView.as_view(),
         name="detail-ticket"),
    path('tickets/create-ticket/', CreateTicketView.as_view(),
         name="create-ticket"),
    path('tickets/update-ticket/<int:pk>', UpdateTicketView.as_view(),
         name="update-ticket"),
    path('tickets/delete-ticket/<int:pk>', delete_ticket_view,
         name="delete-ticket"),
    path('posts/', posts_view, name="posts")
    ]