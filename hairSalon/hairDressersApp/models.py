from datetime import timedelta

from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from hairSalon import settings
from hairSalon.common.models import Service


class AvailableDate(models.Model):
    date = models.DateField(unique=True, help_text="An available date for selection.")

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')

    class Meta:
        verbose_name = "Available Date"
        verbose_name_plural = "Available Dates"
        ordering = ['date']


class Schedule(models.Model):
    WEEKDAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    day_of_week = models.CharField(
        max_length=10,
        choices=WEEKDAYS,
        null=False,
        blank=False,
        unique=True,
        help_text="The recurring day of the week this schedule applies to. Leave blank for a specific date."
    )
    start_time = models.TimeField(help_text="Start time of the working hours.")
    end_time = models.TimeField(help_text="End time of the working hours.")
    slot_duration = models.DurationField(
        default=timedelta(minutes=30),
        help_text="Duration of each appointment slot."
    )
    max_bookings_per_slot = models.PositiveIntegerField(
        default=1,
        help_text="Maximum bookings allowed for each time slot."
    )

    def __str__(self):
        return f"{self.day_of_week}: {self.start_time} - {self.end_time}"


class TimeSlot(models.Model):
    date = models.ForeignKey(
        to=AvailableDate,
        on_delete=models.CASCADE,
        related_name='time_slots',
        help_text="The date of the time slot."
    )
    start_time = models.TimeField(help_text="The start time of the time slot.")
    is_available = models.BooleanField(
        default=True,
        help_text="Whether this slot is available for booking."
    )

    def __str__(self):
        weekday = self.date.date.strftime('%A')
        return f"{weekday} - {self.date} | {self.start_time} | {'Available' if self.is_available else 'Booked'}"

    class Meta:
        verbose_name = "Time Slot"
        verbose_name_plural = "Time Slots"
        unique_together = ('date', 'start_time',)


class Appointment(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    service = models.ForeignKey(
        to=Service,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    date = models.ForeignKey(
        to=AvailableDate,
        on_delete=models.CASCADE,
        related_name='appointments',
    )

    time_slots = models.ForeignKey(
        to=TimeSlot,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    def __str__(self):
        return f"Appointment: {self.client} for {self.service} on {self.time_slots.date} {self.time_slots.start_time}"

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ['time_slots__date',]


@receiver(post_save, sender=Appointment)
def send_appointment_email(sender, instance, created, **kwargs):
    if created:
        user_email = instance.client.email

        subject = "Appointment Confirmation"
        message = (
            f"Dear {instance.client.first_name},\n\n"
            f"Your appointment has been confirmed.\n"
            f"Date: {instance.time_slots.date.date}\n"
            f"Time: {instance.time_slots.start_time}\n\n"
            f"Thank you for booking with us!"
        )

        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False,)
            print(f"Email sent successfully to {user_email}.")
        except Exception as e:
            print(f"Failed to send email to {user_email}: {str(e)}")


@receiver(post_save, sender=Appointment)
def mark_time_slot_as_booked(sender, instance, created, **kwargs):
    if created:
        instance.time_slots.is_available = False
        instance.time_slots.save()
