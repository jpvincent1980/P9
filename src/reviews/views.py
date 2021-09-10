from django.shortcuts import render

from accounts.models import CustomUser
from reviews.models import UserFollows


# Create your views here.
def subscriptions(request):
    current_user = request.user.username
    current_user_id = CustomUser.objects.values_list("id").get(username=current_user)
    followers = UserFollows.objects.filter(followed_user_id=current_user_id).values()
    followers = [follower["user_id"] for follower in followers]
    followed_users = UserFollows.objects.filter(user_id=current_user_id).values()
    followed_users = [user["followed_user_id"] for user in followed_users]
    followers = [CustomUser.objects.get(pk=follower_id) for follower_id in followers]
    followed_users = [CustomUser.objects.get(pk=user_id) for user_id in followed_users]
    context = {"followers": followers,
               "followed_users": followed_users}
    return render(request, "reviews/subscriptions.html", context)