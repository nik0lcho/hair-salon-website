from datetime import timedelta, date, datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class AvailableDate(models.Model):
    date = models.DateField(unique=True, help_text="An available date for selection.")

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')

    class Meta:
        verbose_name = "Available Date"
        verbose_name_plural = "Available Dates"
        ordering = ['date']


class Schedule(models.Model):
    """
    Represents a recurring weekly schedule or a one-time specific date schedule.
    """
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
        null=True,
        blank=True,
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
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether the schedule is currently active."
    )

    def __str__(self):
        return f"{self.day_of_week}: {self.start_time} - {self.end_time}"

    def generate_time_slots(self, days_ahead=30):
        from_date = date.today()
        end_date = from_date + timedelta(days=days_ahead)

        for current_date in (from_date + timedelta(days=i) for i in range((end_date - from_date).days + 1)):
            # Only process dates that match the schedule's day_of_week
            if current_date.strftime('%A') != self.day_of_week:
                continue

            # Create or retrieve the AvailableDate

            available_date, created = AvailableDate.objects.get_or_create(date=current_date)

            # Generate time slots for this AvailableDate
            current_time = datetime.combine(available_date.date, self.start_time)
            end_time = datetime.combine(available_date.date, self.end_time)

            while current_time + self.slot_duration <= end_time:
                TimeSlot.objects.get_or_create(
                    date=available_date,  # Linking the time slot to AvailableDate
                    start_time=current_time.time(),
                )
                current_time += self.slot_duration


class TimeSlot(models.Model):
    """
    Represents a specific time slot on a given date.
    """
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


@receiver(post_save, sender=Schedule)
def generate_slots_for_schedule(sender, instance, created, **kwargs):
    """
    Generate time slots when a schedule is created or updated.
    """
    if instance.is_active:
        instance.generate_time_slots()


class DeactivateTimeSlots(models.Model):
    """
    Represents a request to deactivate all time slots within a specific date range.
    """
    start_date = models.DateField(help_text="Start date for the period to deactivate time slots.")
    end_date = models.DateField(help_text="End date for the period to deactivate time slots.")
    reason = models.TextField(help_text="Optional reason for deactivating the time slots.", blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Indicates whether the deactivation is still active or not.")

    def __str__(self):
        return f"Deactivate Slots from {self.start_date} to {self.end_date}"

    def deactivate_slots(self):
        """
        Deactivate all time slots within the specified date range.
        """
        # Deactivate all time slots within the date range
        time_slots = TimeSlot.objects.filter(date__range=[self.start_date, self.end_date])
        updated_count = time_slots.update(is_available=False)

        return updated_count  # Return the count of updated slots

    def save(self, *args, **kwargs):
        # Optionally, deactivates time slots automatically when saved
        super().save(*args, **kwargs)
        if self.is_active:
            self.deactivate_slots()

    class Meta:
        verbose_name_plural = "Deactivate Time Slots"
