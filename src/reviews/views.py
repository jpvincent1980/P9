from django.shortcuts import render


# Create your views here.
def subscriptions(request):
    context = {}
    return render(request, "reviews/subscriptions.html", context)