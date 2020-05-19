from django import forms
from .models import Size
from django.utils.translation import gettext_lazy as _


class SizeChooseForm(forms.Form):
    sizes = forms.ModelChoiceField(
        queryset=Size.objects.none())


