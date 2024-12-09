from django.shortcuts import render
from hairSalon.hairDressersApp.models import Schedule


# Create your views here.

def home(request):
    return render(request, 'home.html')


