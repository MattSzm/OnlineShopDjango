from django import forms
from .models import Size


class SizeChooseForm(forms.Form):
    sizes = forms.ModelChoiceField(
        queryset=Size.objects.none())


