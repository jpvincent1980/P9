from django.contrib import admin

from reviews.models import Ticket, Review


# Register your models here.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
