from django.urls import path
from .views import get_timeslots, get_available_dates

urlpatterns = [
    path('get-timeslots/', get_timeslots, name='get_timeslots'),
    path('get-available-dates/', get_available_dates, name='get_available_dates')
]
