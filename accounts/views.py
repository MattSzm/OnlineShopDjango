from django.shortcuts import render, get_list_or_404
from . import forms
from django.core.mail import send_mail
from django.views.generic.base import TemplateResponseMixin, View
from .forms import UserChangeDataForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from cart import models as cartModels
from .models import ShopUser


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
                body = 'We are happy, you are with us! You can login here: {} .\n\n ' \
                       'OnlineShop Team'.format(login_url)
                send_mail(title, body, 'testmateusz1234@gmail.com', [new_user.email])

                return render(request, 'registration/register_done.html',
                            {'new_user':  new_user})
            except:
                #TODO: message that there is already somebody with this email
                pass
    form = forms.UserRegisterForm()
    return render(request, 'registration/register.html',
                      {'form': form})


class userDashboard(TemplateResponseMixin, View):
    model = ShopUser
    template_name = 'maintenance/profileEdit.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('%s?next=%s' % (reverse('accounts:login'),
                                                reverse('cart:createOrder')))

        form = UserChangeDataForm(instance=request.user)
        orders = cartModels.Order.objects.filter(user=request.user)

        return self.render_to_response({'form': form,
                                        'orders': orders})


    def post(self, request):
        pass
        #todo: implement in future!!!!