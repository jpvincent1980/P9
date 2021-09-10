from django.urls import path
from accounts.views import SignupView,account_created, index_view, logout_view

# Création d'un espace de noms
app_name = 'accounts'

urlpatterns = [
    path('', index_view, name="index"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('account-created/', account_created, name="account-created"),
    path('logout/', logout_view, name="logout")
]