from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from PIL import Image

from LITReview import settings


# Create your models here.
class Ticket(models.Model):
    """
    A model that represents a ticket
    """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="reviews")
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Displays the ticket's title when ticket is printed

        Returns: a string (the title field)

        """
        return self.title

    @property
    def max_width(self):
        """
        Returns the maximum between the image width or 400.
        Used to display the image properly in templates.

        Returns: an integer

        """
        if self.image.width > 400:
            return 400
        return self.image.width

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        Overrides the save method to update image size at upload to limit width
        and height

        Args:
            force_insert: False
            force_update: False
            using: None
            update_fields: None

        Returns: Nothing

        """
        super(Ticket,self).save(force_insert=False,
                                force_update=False,
                                using=None,
                                update_fields=None)
        if self.image:
            updated_image = Image.open(self.image)
            if updated_image.width > 400 or updated_image.height > 250:
                output_size = (400,250)
                updated_image.thumbnail(output_size)
                updated_image.save(self.image.path)


class Review(models.Model):
    """
    A model that represents a review
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                          MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Displays the review's headline when review is printed

        Returns: a string (the headline field)

        """
        return self.headline

    @property
    def stars(self):
        """
        A property that represents the review rating as a string made of stars

        Returns: a string made of 1 up to 5 stars

        """
        return "".join(["🟊" for _ in range(self.rating)])
