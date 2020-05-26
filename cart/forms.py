from django import forms
from .models import Order

QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]

class CartChangeQuantity(forms.Form):
    quantity = forms.TypedChoiceField(choices = QUANTITY_CHOICES,
                                      coerce=int)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('deliveredToAnotherAddress',
                  'firstNameD','lastNameD','addressD','cityD',
                  'zipCodeD','telephoneNumberD','extraInfoD')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['firstNameD'].required = False
        self.fields['lastNameD'].required = False
        self.fields['addressD'].required = False
        self.fields['cityD'].required = False
        self.fields['zipCodeD'].required = False
        self.fields['telephoneNumberD'].required = False
        self.fields['extraInfoD'].required = False
