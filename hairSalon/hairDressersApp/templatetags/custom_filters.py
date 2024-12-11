from django import template
from django.utils import timezone
from datetime import datetime, timedelta

register = template.Library()


@register.filter
def can_cancel(appointment):

    appointment_date = appointment.date.date
    appointment_datetime = timezone.make_aware(datetime.combine(appointment_date, appointment.time_slots.start_time))

    now = timezone.now()

    time_left = appointment_datetime - now
    return time_left.total_seconds() > 7200


@register.filter
def can_display_appointment(appointment):

    appointment_datetime = timezone.make_aware(
        datetime.combine(appointment.date.date, appointment.time_slots.start_time)
    )
    now = timezone.now()
    time_diff = now - appointment_datetime

    return time_diff <= timedelta(minutes=20)
