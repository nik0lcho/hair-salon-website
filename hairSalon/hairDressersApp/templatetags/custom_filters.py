# hairDressersApp/templatetags/custom_filters.py

from django import template
from django.utils import timezone
from datetime import datetime

register = template.Library()


@register.filter
def can_cancel(appointment):
    """
    This filter checks if the appointment time is more than 2 hours away from now.
    """
    # Access the date from the AvailableDate model (appointment.date is a ForeignKey to AvailableDate)
    appointment_date = appointment.date.date

    # Combine the date and time to form a datetime object for the appointment
    # appointment_date is already a date, and appointment.time_slots.start_time is a time object
    appointment_datetime = timezone.make_aware(datetime.combine(appointment_date, appointment.time_slots.start_time))

    # Get the current time (timezone-aware)
    now = timezone.now()

    # Check if the appointment is more than 2 hours away
    time_left = appointment_datetime - now
    return time_left.total_seconds() > 7200  # Return True if more than 2 hours
