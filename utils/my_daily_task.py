import os
import django
from datetime import timedelta, date, datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hairSalon.settings')
django.setup()

# Import required models
from hairSalon.hairDressersApp.models import Schedule, AvailableDate, TimeSlot


def delete_old_time_slots_and_dates():
    """
    Deletes time slots and associated AvailableDate objects for dates before today.
    """
    yesterday = date.today() - timedelta(days=1)

    # Find all AvailableDates before today
    old_dates = AvailableDate.objects.filter(date__lte=yesterday)

    for old_date in old_dates:
        # Delete all TimeSlots related to this AvailableDate
        old_date.time_slots.all().delete()

        # Delete the AvailableDate itself
        old_date.delete()


def generate_time_slots_for_schedule(schedule, days_ahead=30):
    """
    Generates time slots for a given schedule for the next `days_ahead` days.
    """
    from_date = date.today()
    end_date = from_date + timedelta(days=days_ahead)

    for current_date in (from_date + timedelta(days=i) for i in range((end_date - from_date).days + 1)):
        # Only process dates that match the schedule's day_of_week
        if current_date.strftime('%A') != schedule.day_of_week:
            continue

        # Create or retrieve the AvailableDate
        available_date, created = AvailableDate.objects.get_or_create(date=current_date)

        # Generate time slots for this AvailableDate
        current_time = datetime.combine(available_date.date, schedule.start_time)
        end_time = datetime.combine(available_date.date, schedule.end_time)

        while current_time + schedule.slot_duration <= end_time:
            TimeSlot.objects.get_or_create(
                date=available_date,  # Linking the time slot to AvailableDate
                start_time=current_time.time(),
            )
            current_time += schedule.slot_duration


def generate_time_slots_for_all_schedules(days_ahead=30):
    """
    Generates time slots for all schedules in the database for the next `days_ahead` days.
    """
    schedules = Schedule.objects.all()
    for schedule in schedules:
        generate_time_slots_for_schedule(schedule, days_ahead)


if __name__ == "__main__":
    # Delete old time slots and associated dates
    delete_old_time_slots_and_dates()

    # Generate new time slots
    generate_time_slots_for_all_schedules(days_ahead=30)
