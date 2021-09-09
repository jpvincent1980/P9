from django.urls import path
from accounts.views import SignupView, index, account_created

# Création d'un espace de noms
app_name = 'accounts"'

urlpatterns = [
    path('', index, name="index"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('account-created/', account_created, name="account-created")
]