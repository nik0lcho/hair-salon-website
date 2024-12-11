from django.urls import path

from . import views
from .views import get_timeslots, get_available_dates

urlpatterns = [
    path('get-timeslots/', get_timeslots, name='get_timeslots'),
    path('get-available-dates/', get_available_dates, name='get_available_dates'),
    path('about/', views.ScheduleListView.as_view(), name='about'),
    path('appointments/', views.AppointmentListView.as_view(), name='appointments'),
    path('cancel-appointment/<int:appointment_id>/', views.CancelAppointmentView.as_view(), name='cancel_appointment'),
    path('make-appointment/', views.MakeAppointmentView.as_view(), name='make_appointment'),
    path('salon-appointments/', views.SalonAppointmentListView.as_view(), name='salon_appointments')
]
