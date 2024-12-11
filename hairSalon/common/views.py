from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.


def home(request):
    return render(request, 'home.html')


def custom_403(request, exception=None):
    return redirect('home')
