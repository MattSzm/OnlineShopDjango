from django.shortcuts import render, redirect
from . import forms
from django.core.mail import send_mail
from django.views.generic.base import TemplateResponseMixin, View
from .forms import UserChangeDataForm
from django.http import HttpResponseRedirect
from cart import models as cartModels
from .models import ShopUser
from django.urls import reverse
from django.contrib import messages
from django.conf import settings


def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                new_user = form.save(commit=False)
                new_user.set_password(
                    form.cleaned_data['password'])
                new_user.save()

                login_url = request.build_absolute_uri('/account/login/')
                short_name = new_user.email.split('@')[0]
                title = 'Thank you {} for registration - OnlineShop'.format(short_name)
                body = 'We are happy, you are with us! You can login here: {} .\n\n' \
                       'OnlineShop Team'.format(login_url)
                send_mail(title, body, settings.EMAIL_HOST_USER, [new_user.email])

                return render(request, 'registration/register_done.html',
                            {'new_user':  new_user})
            except:
                messages.error(request, 'There is already somebody with this email.')
        else:
            try:
                form.clean_password_confirmation()
                messages.error(request, 'There is already somebody with this email.')
            except:
                messages.error(request, 'The passwords are different.')

    form = forms.UserRegisterForm()
    return render(request, 'registration/register.html',
                        {'form': form})


class userDashboard(TemplateResponseMixin, View):
    model = ShopUser
    template_name = 'maintenance/profileEdit.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('%s?next=%s' % (reverse('accounts:login'),
                                                reverse('accounts:dashboard')))

        form = UserChangeDataForm(instance=request.user)
        orders = cartModels.Order.objects.filter(user=request.user)
        orders = orders.filter(paid=True)

        return self.render_to_response({'form': form,
                                        'orders': orders,
                                        'section': 'myaccount'})

    def post(self, request):
        form  = UserChangeDataForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modification completed successfully.')
        else:
            messages.error(request, 'You need to enter the correct data')
        return redirect(reverse('accounts:dashboard'))

