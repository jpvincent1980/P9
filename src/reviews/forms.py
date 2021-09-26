from django.forms import ModelForm, ChoiceField, RadioSelect
from django.forms.widgets import FileInput
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, ugettext_lazy

from reviews.models import Review, Ticket

# In reverse order on purpose so that star rating system works
CHOICES = [(5, ""), (4, ""), (3, ""), (2, ""), (1, "")]


class ReviewForm(ModelForm):
    """
    A form inheriting from ModelForm to create a Review instance.
    """
    rating = ChoiceField(label="Votre note",
                         choices=CHOICES,
                         widget=RadioSelect)

    class Meta:
        model = Review
        fields = ["headline","rating","body"]
        labels = {"headline": _("Titre"),
                  "body": _("Votre critique")}


class UpdateReviewForm(ModelForm):
    """
    A form inheriting from ModelForm to update a Review instance.
    """
    rating = ChoiceField(label="Votre note",
                         choices=CHOICES,
                         widget=RadioSelect)

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        labels = {"headline": _("Titre"),
                  "body": _("Votre critique")}


class TicketForm(ModelForm):
    """
    A form inheriting from ModelForm to create a Ticket instance.
    """
    class Meta:
        model = Ticket
        exclude = ["user"]
        labels = {"title": "Titre"}


class CustomImageFieldWidget(FileInput):
    """
    A class inheriting from FileInput to customize html output of ImageField
    """
    initial_text = ugettext_lazy('Image actuelle')
    input_text = ugettext_lazy('Nouvelle image')
    template_with_initial = '<p>%(initial_text)s: </p><p>%(initial)s </p>' \
                            '<p>%(input_text)s: </p><p>%(input)s </p>'
    url_markup_template = '<img src="{0}" alt="{1}"/>'

    def render(self, name, value, attrs=None, renderer=None):
        substitutions = {'initial_text': self.initial_text,
                         'input_text': self.input_text,}
        template = '%(input)s'
        substitutions['input'] = super(CustomImageFieldWidget, self).render(
            name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = format_html(self.url_markup_template,
                                                   value.url,
                                                   force_text(value))

        return mark_safe(template % substitutions)


class UpdateTicketForm(ModelForm):
    """
    A form inheriting from ModelForm to update a Ticket instance.
    """
    class Meta:
        model = Ticket
        exclude = ["user"]
        labels = {"title": "Titre"}
        widgets = {"image": CustomImageFieldWidget}
