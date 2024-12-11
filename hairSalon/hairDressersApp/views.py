from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import ListView, View
from .models import TimeSlot, AvailableDate, Schedule
from django.shortcuts import get_object_or_404
from django.contrib import messages
from datetime import datetime, timedelta
import pytz
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Appointment
from .forms import AppointmentForm
from datetime import date
from .templatetags.custom_filters import can_display_appointment


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointments = context['appointments']

        # Add the 'displayed' flag to the context
        displayed = False

        # Check if any appointment passes the can_display_appointment filter
        for appointment in appointments:
            if can_display_appointment(appointment):
                displayed = True
                break  # No need to continue checking once we find one appointment to display

        # Add the 'displayed' flag to the context
        context['displayed'] = displayed

        return context


class CancelAppointmentView(View):
    template_name = 'cancel_appointment.html'  # Confirmation page template
    success_url = reverse_lazy('appointments')  # Redirect after successful cancel

    def get(self, request, *args, **kwargs):
        """
        Load the confirmation page.
        """
        appointment = get_object_or_404(Appointment, id=kwargs.get('appointment_id'))

        # Ensure the user is authorized to cancel the appointment
        if appointment.client != request.user:
            messages.error(request, "You are not authorized to cancel this appointment.")
            return redirect('appointments')

        return render(request, self.template_name, {'appointment': appointment})

    def post(self, request, *args, **kwargs):
        """
        Handle the cancellation confirmation.
        """
        appointment = get_object_or_404(Appointment, id=kwargs.get('appointment_id'))

        # Ensure the user is authorized to cancel the appointment
        if appointment.client != request.user:
            messages.error(request, "You are not authorized to cancel this appointment.")
            return redirect('appointments')

        # Calculate appointment datetime
        appointment_datetime = datetime.combine(appointment.date.date, appointment.time_slots.start_time)
        appointment_datetime = timezone.make_aware(appointment_datetime, timezone.get_current_timezone())

        # Check if it's too late to cancel (2 hours before the appointment)
        if appointment_datetime - timezone.now() < timedelta(hours=2):
            messages.error(request, "You cannot cancel this appointment less than 2 hours before its start time.")
            return redirect('appointments')

        # Free the associated time slot
        time_slot = appointment.time_slots
        time_slot.is_available = True
        time_slot.save()

        # Delete the appointment
        appointment.delete()

        # Notify the user of successful cancellation
        messages.success(request, "Appointment canceled successfully, and the time slot is now available.")
        return redirect(self.success_url)


class MakeAppointmentView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'make_appointment.html'
    success_url = reverse_lazy('appointments')  # Redirect to a page listing all appointments

    def form_valid(self, form):
        form.instance.client = self.request.user  # Automatically assign the current user as the client
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))
