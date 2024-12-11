# hairDressersApp/templatetags/custom_filters.py

from django import template
from django.utils import timezone
from datetime import datetime, timedelta

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


@register.filter
def can_display_appointment(appointment):
    """
    Checks if the appointment is within the allowed time (e.g., 20 minutes after its start time).
    If it is, the appointment will be displayed; otherwise, it won't.
    """
    # Combine the appointment's date and time to create a datetime object
    appointment_datetime = timezone.make_aware(
        datetime.combine(appointment.date.date, appointment.time_slots.start_time)
    )

    # Calculate the time difference between now and the appointment's start time
    now = timezone.now()

    # Define the time difference threshold (e.g., 20 minutes after start)
    time_diff = now - appointment_datetime

    # Return True if the appointment is still valid (within the allowed time), False otherwise
    return time_diff <= timedelta(minutes=20)
