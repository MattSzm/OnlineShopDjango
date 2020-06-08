from django import forms
from .models import Size
from django.utils.translation import gettext_lazy as _

class SizeChooseForm(forms.Form):
    sizes = forms.ModelChoiceField(
        queryset=Size.objects.none(),
        label=_('Size'))

class searchingForm(forms.Form):
    input = forms.CharField(label=_('What are you looking for?'),
                widget=forms.TextInput(attrs={'placeholder':
                                    'What are you looking for?'}),
                            max_length=100)


