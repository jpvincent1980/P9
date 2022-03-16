from django.contrib import admin

from accounts.models import CustomUser, UserFollows


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage Users instances in the Admin
    interface.
    """
    list_display = ("id", "username")
    list_editable = ("username",)


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage UserFollows instances in the
    Admin interface.
    """
    pass
