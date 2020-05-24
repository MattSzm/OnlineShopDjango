from django.shortcuts import render
from . import forms


def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                new_user = form.save(commit=False)
                new_user.set_password(
                    form.cleaned_data['password'])
                new_user.save()
                return render(request, 'registration/register_done.html',
                            {'new_user':  new_user})
            except:
                #TODO: message that there is already somebody with this email
                pass
    form = forms.UserRegisterForm()
    return render(request, 'registration/register.html',
                      {'form': form})
