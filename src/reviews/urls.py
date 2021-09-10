from django.urls import path
from reviews.views import subscriptions


# Création d'un espace de noms
app_name = 'reviews'

urlpatterns = [
    path('subscriptions/', subscriptions, name="subscriptions")
    ]