from django.urls import path

from reviews.views import UpdateReviewView, CreateTicketView, \
    UpdateTicketView, create_review_view, posts_view, DeleteTicketView

# Création d'un espace de noms
app_name = 'reviews'

urlpatterns = [
    path('reviews/create-review/', create_review_view, name="create-review"),
    path('reviews/create-review/<int:ticket_id>', create_review_view, name="create-review"),
    path('reviews/update-review/<int:review_id>', UpdateReviewView.as_view(), name="update-review"),
    path('reviews/create-ticket/', CreateTicketView.as_view(), name="create-ticket"),
    path('reviews/update-ticket/<int:ticket_id>', UpdateTicketView.as_view(), name="update-ticket"),
    path('reviews/delete-ticket/<int:ticket_id>', DeleteTicketView.as_view(), name="delete-ticket"),
    path('posts/', posts_view, name="posts")
    ]