from django.conf import settings
from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.db import models


class CustomUser(AbstractUser):
    pass


class UserFollows(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='following')
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='followed_by')

    def __str__(self):
        return self.user.username + " abonné à " + self.followed_user.username

    class Meta:
        unique_together = ('user', 'followed_user')
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
