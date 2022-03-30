from django.shortcuts import render


def index(request):
    return render(request, 'motivator/index.html', {'title': 'Home'})


def goals(request):
    return render(request, 'motivator/goals.html')
