from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'account created for {username}!')

            return HttpResponseRedirect('/goals')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'title': 'Register', 'form': form})
