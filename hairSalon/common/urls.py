from django.urls import path

from hairSalon.common import views

urlpatterns = [
    path('', views.home, name='home'),
]
