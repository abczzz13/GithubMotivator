from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import RegisterForm


# Create your views here.
def index(request):
    return render(request, 'motivator/index.html', {'title': 'Home'})


def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.post)

        if form.is_valid():

            return HttpResponseRedirect('/motivator/goals.html')
    else:
        form = RegisterForm
    return render(request, 'motivator/register.html', {'title': 'Register', 'form': form})


def goals(request):
    return render(request, 'motivator/goals.html')
