from django.http import JsonResponse
from django.views.generic import ListView, DeleteView
from .models import TimeSlot, AvailableDate, Schedule, Appointment
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.timezone import now
from datetime import datetime, timedelta
import pytz

from datetime import date


def get_available_dates(request):
    """
    Fetch all available dates for selection, filtering out past dates.
    """
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Get today's date
        today = date.today()

        # Filter the available dates to include only those that are greater than or equal to today
        available_dates = AvailableDate.objects.filter(date__gte=today).values('id', 'date')

        return JsonResponse({
            'available_dates': [{'id': date_obj['id'], 'display': date_obj['date'].strftime("%Y-%m-%d")} for date_obj in
                                available_dates]
        })
    return JsonResponse({"error": "Invalid request"}, status=400)


def get_timeslots(request):
    """
    Fetch all available time slots for a selected date.
    If it's today, filter by both date and time; if not, only by date.
    """
    date_id = request.GET.get('date')  # This is the date_id, not the date string
    try:
        if not date_id:
            raise ValueError("Date ID is required.")

        # Retrieve the date from AvailableDate using the date_id
        available_date = AvailableDate.objects.get(id=date_id)
        selected_date = available_date.date  # The actual date from AvailableDate

        # Sofia/Bulgaria timezone (UTC +2)
        sofia_tz = pytz.timezone('Europe/Sofia')

        # Get today's date in Sofia timezone (make it aware if it's naive)
        today = datetime.now(sofia_tz).date()

        # If the selected date is today, filter based on both date and time
        if selected_date == today:
            # Get the current time in Sofia timezone
            current_time = datetime.now(sofia_tz).time()

            # Filter for available timeslots later than or equal to the current time
            timeslots = TimeSlot.objects.filter(
                is_available=True,
                date__date=selected_date,  # Filter by the selected date
                start_time__gte=current_time  # Filter by time for today
            )
        else:
            # If the selected date is not today, filter only by the selected date (no time filter)
            timeslots = TimeSlot.objects.filter(
                is_available=True,
                date__date=selected_date  # Only filter by date
            )

        return JsonResponse({
            'time_slots': [{'id': ts.id, 'display': str(ts)} for ts in timeslots]  # Return time slots as str
        })

    except AvailableDate.DoesNotExist:
        return JsonResponse({'error': 'Invalid date ID.'}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date ID or no time slots available.'}, status=400)

class ScheduleListView(ListView):
    model = Schedule
    template_name = "about.html"  # Specify your template
    context_object_name = 'schedules'  # Name to use in the template

    def get_queryset(self):
        # Get all schedules
        schedules = Schedule.objects.all()

        # Define the correct order of days of the week
        weekdays_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Order the schedules by the correct weekday order
        schedules = sorted(schedules, key=lambda x: weekdays_order.index(x.day_of_week) if x.day_of_week else 7)

        return schedules


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        # Filter appointments for the logged-in user
        return Appointment.objects.filter(client=self.request.user)


class CancelAppointmentView(DeleteView):
    model = Appointment
    template_name = 'cancel_appointment.html'  # Optional confirmation page
    success_url = reverse_lazy('appointments')

    def get(self, request, *args, **kwargs):
        """
        Optionally confirm before deletion.
        """
        appointment = self.get_object()
        appointment_datetime = datetime.combine(appointment.date.date, appointment.time_slots.start_time)

        # Check if the appointment can still be canceled
        if appointment_datetime - now() < timedelta(hours=2):
            messages.error(self.request, "You cannot cancel this appointment less than 2 hours before its start time.")
            return redirect('appointments')

        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Cancel the appointment and free the associated time slot.
        """
        appointment = self.get_object()

        # Ensure the user is authorized
        if appointment.client != self.request.user:
            messages.error(request, "You are not authorized to cancel this appointment.")
            return redirect('appointments')

        # Check the time restriction
        appointment_datetime = datetime.combine(appointment.date.date, appointment.time_slots.start_time)
        if appointment_datetime - now() < timedelta(hours=2):
            messages.error(request, "You cannot cancel this appointment less than 2 hours before its start time.")
            return redirect('appointments')

        # Free the associated time slot
        time_slots = appointment.time_slots
        time_slots.is_available = True
        time_slots.save()

        # Delete the appointment
        appointment.delete()

        # Notify the user
        messages.success(request, "Appointment canceled successfully, and the time slot is now available.")
        return redirect(self.success_url)
