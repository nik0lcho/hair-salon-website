from django.urls import path
from .views import get_timeslots

urlpatterns = [
    path('get-timeslots/', get_timeslots, name='get_timeslots'),
]
