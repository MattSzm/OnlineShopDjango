from django.shortcuts import render
from . import forms
from django.core.mail import send_mail


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
