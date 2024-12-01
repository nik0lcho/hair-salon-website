from django.db import models
from datetime import timedelta, date, datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    specific_date = models.DateField(
        null=True,
        blank=True,
        help_text="Specific date for this schedule. Overrides the weekly schedule for that date."
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
        if self.specific_date:
            return f"Specific Date: {self.specific_date} | {self.start_time} - {self.end_time}"
        return f"{self.day_of_week}: {self.start_time} - {self.end_time}"

    def generate_time_slots(self, from_date=None, days_ahead=30):
        """
        Generate time slots for the next `days_ahead` days or a specific date.
        """
        if self.specific_date:
            # Generate only for the specific date
            self._generate_slots_for_date(self.specific_date)
            return

        if not from_date:
            from_date = date.today()

        end_date = from_date + timedelta(days=days_ahead)
        current_date = from_date

        while current_date <= end_date:
            if current_date.strftime('%A') == self.day_of_week and self.is_active:
                self._generate_slots_for_date(current_date)
            current_date += timedelta(days=1)

    def _generate_slots_for_date(self, target_date):
        """
        Generate time slots for a specific date.
        """
        current_time = datetime.combine(target_date, self.start_time)
        end_time = datetime.combine(target_date, self.end_time)

        while current_time + self.slot_duration <= end_time:
            TimeSlot.objects.get_or_create(
                date=current_time.date(),
                start_time=current_time.time(),
                schedule=self,
                defaults={'is_available': True}
            )
            current_time += self.slot_duration


class TimeSlot(models.Model):
    """
    Represents a specific time slot on a given date.
    """
    date = models.DateField(help_text="The date of the time slot.")
    start_time = models.TimeField(help_text="The start time of the time slot.")
    is_available = models.BooleanField(
        default=True,
        help_text="Whether this slot is available for booking."
    )
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name="time_slots",
        help_text="The schedule this time slot belongs to."
    )

    def __str__(self):
        weekday = self.date.strftime('%A')
        return f"{weekday} - {self.date} | {self.start_time} | {'Available' if self.is_available else 'Booked'}"

    class Meta:
        verbose_name = "Time Slot"
        verbose_name_plural = "Time Slots"
        unique_together = ('date', 'start_time', 'schedule')


# Signal to generate time slots when a schedule is created or updated
@receiver(post_save, sender=Schedule)
def generate_slots_for_schedule(sender, instance, created, **kwargs):
    """
    Generate time slots when a schedule is created or updated.
    """
    if instance.is_active:
        instance.generate_time_slots()
