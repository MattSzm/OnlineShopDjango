from django import forms
from .models import ShopUser
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label=_('Password'),
        min_length=6)
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput,
        label=_('Password confirmation'),
        min_length=6)

    class Meta:
        model = ShopUser
        fields = ('email','firstName','lastName',
                  'address', 'city','zipCode',
                  'telephoneNumber','photo',)

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['firstName'].required = False
        self.fields['lastName'].required = False
        self.fields['address'].required = False
        self.fields['zipCode'].required = False
        self.fields['telephoneNumber'].required = False
        self.fields['photo'].required = False
        self.fields['city'].required = False

    def clean_password_confirmation(self):
        cleandata = self.cleaned_data
        if cleandata['password'] != cleandata['password_confirmation']:
            raise forms.ValidationError('Passwords do not match')
        return cleandata['password']


class UserChangeDataForm(forms.ModelForm):
    class Meta:
        model = ShopUser
        fields = (('email','firstName','lastName',
                  'address', 'city','zipCode',
                  'telephoneNumber', 'photo',))

    def __init__(self, *args, **kwargs):
        super(UserChangeDataForm, self).__init__(*args, **kwargs)
        self.fields['firstName'].required = False
        self.fields['lastName'].required = False
        self.fields['address'].required = False
        self.fields['zipCode'].required = False
        self.fields['telephoneNumber'].required = False
        self.fields['photo'].required = False
        self.fields['city'].required = False
