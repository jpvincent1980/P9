from django.forms import ModelForm, ChoiceField, RadioSelect
from django.utils.translation import gettext_lazy as _

from reviews.models import Review, Ticket


class ReviewForm(ModelForm):
    CHOICES = [(1,""),
               (2,""),
               (3,""),
               (4,""),
               (5,"")]
    rating = ChoiceField(label="Votre note", choices=CHOICES, widget=RadioSelect)

    class Meta:
        model = Review
        fields = ["headline","rating","body"]
        labels = {"headline": _("Titre"),
                  "body": _("Votre critique")}


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = ["user"]
        labels = {"title": "Titre"}
