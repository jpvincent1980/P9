from django.urls import path
from accounts.views import SignupView, index_view, logout_view, \
    account_created_view, subscriptions_view, unsubscribe_view, subscribe_view, \
    login_view

# Création d'un espace de noms
app_name = 'accounts'

urlpatterns = [
    path('', index_view, name="index"),
    path('login/', login_view, name="login"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('account-created/', account_created_view, name="account-created"),
    path('logout/', logout_view, name="logout"),
    path('subscriptions/', subscriptions_view, name="subscriptions"),
    path('unsubscribe/<int:user_id>', unsubscribe_view, name="unsubscribe"),
    path('subscribe/<int:user_id>', subscribe_view, name="subscribe")
]