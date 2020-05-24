from django import forms

QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]

class CartChangeQuantity(forms.Form):
    quantity = forms.TypedChoiceField(choices = QUANTITY_CHOICES,
                                      coerce=int)
