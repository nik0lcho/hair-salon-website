from datetime import datetime, timedelta, date
import pytz

from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView

from utils.decorators import role_required
from .models import TimeSlot, AvailableDate, Schedule, Appointment
from .forms import AppointmentForm
from .templatetags.custom_filters import can_display_appointment


def get_available_dates(request):
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        today = date.today()
        available_dates = AvailableDate.objects.filter(date__gte=today).values('id', 'date')

        return JsonResponse({
            'available_dates': [{'id': date_obj['id'], 'display': date_obj['date'].strftime("%Y-%m-%d")} for date_obj in
                                available_dates]
        })
    return JsonResponse({"error": "Invalid request"}, status=400)


def get_timeslots(request):
    date_id = request.GET.get('date')
    try:
        if not date_id:
            raise ValueError("Date ID is required.")

        available_date = AvailableDate.objects.get(id=date_id)
        selected_date = available_date.date

        sofia_tz = pytz.timezone('Europe/Sofia')
        today = datetime.now(sofia_tz).date()

        if selected_date == today:
            current_time = datetime.now(sofia_tz).time()

            timeslots = TimeSlot.objects.filter(
                is_available=True,
                date__date=selected_date,
                start_time__gte=current_time
            )
        else:
            timeslots = TimeSlot.objects.filter(
                is_available=True,
                date__date=selected_date
            )

        return JsonResponse({
            'time_slots': [{'id': ts.id, 'display': str(ts)} for ts in timeslots]
        })

    except AvailableDate.DoesNotExist:
        return JsonResponse({'error': 'Invalid date ID.'}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date ID or no time slots available.'}, status=400)


class ScheduleListView(ListView):
    model = Schedule
    template_name = "about.html"
    context_object_name = 'schedules'

    def get_queryset(self):
        schedules = Schedule.objects.all()

        weekdays_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        schedules = sorted(schedules, key=lambda x: weekdays_order.index(x.day_of_week) if x.day_of_week else 7)

        return schedules


@method_decorator(role_required('Client', 'Staff'), name='dispatch')
class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(client=self.request.user).order_by('date__date', 'time_slots__start_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointments = context['appointments']

        displayed = False

        for appointment in appointments:
            if can_display_appointment(appointment):
                displayed = True
                break

        context['displayed'] = displayed

        return context


@method_decorator(role_required('Client', 'Staff'), name='dispatch')
class CancelAppointmentView(View):
    template_name = 'cancel_appointment.html'
    success_url = reverse_lazy('appointments')

    def get(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, id=kwargs.get('appointment_id'))

        if appointment.client != request.user:
            messages.error(request, "You are not authorized to cancel this appointment.")
            return redirect('appointments')

        return render(request, self.template_name, {'appointment': appointment})

    def post(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, id=kwargs.get('appointment_id'))

        if appointment.client != request.user:
            messages.error(request, "You are not authorized to cancel this appointment.")
            return redirect('appointments')

        appointment_datetime = datetime.combine(appointment.date.date, appointment.time_slots.start_time)
        appointment_datetime = timezone.make_aware(appointment_datetime, timezone.get_current_timezone())

        if appointment_datetime - timezone.now() < timedelta(hours=2):
            messages.error(request, "You cannot cancel this appointment less than 2 hours before its start time.")
            return redirect('appointments')

        time_slot = appointment.time_slots
        time_slot.is_available = True
        time_slot.save()

        appointment.delete()

        messages.success(request, "Appointment canceled successfully, and the time slot is now available.")
        return redirect(self.success_url)


@method_decorator(role_required('Client', 'Staff'), name='dispatch')
class MakeAppointmentView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'make_appointment.html'
    success_url = reverse_lazy('appointments')

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(role_required('Hairdresser', 'Staff'), name='dispatch')
class SalonAppointmentListView(ListView):
    model = Appointment
    template_name = 'salon-appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.order_by('date__date', 'time_slots__start_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointments = context['appointments']

        displayed = False

        for appointment in appointments:
            if can_display_appointment(appointment):
                displayed = True
                break

        context['displayed'] = displayed

        return context
