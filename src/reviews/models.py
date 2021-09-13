from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from LITReview import settings


# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="reviews")
    time_created = models.DateTimeField(auto_now_add=True)

    @property
    def max_width(self):
        if self.image.width > 400:
            return 400
        return self.image.width


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                          MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
