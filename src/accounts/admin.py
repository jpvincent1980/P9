from django.contrib import admin

from accounts.models import CustomUser, UserFollows


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")
    list_editable = ("username",)


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    pass

