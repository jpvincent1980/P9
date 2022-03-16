from django.contrib import admin
from django.utils.safestring import mark_safe

from reviews.models import Ticket, Review


# Register your models here.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ["aperçu_image"]

    def aperçu_image(self, obj):
        return mark_safe("<img src='{url}' />".format(url=obj.image.url))


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
