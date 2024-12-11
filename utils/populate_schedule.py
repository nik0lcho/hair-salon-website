import os
import django
from datetime import datetime, timedelta, time

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hairSalon.settings')
django.setup()

from hairSalon.hairDressersApp.models import Schedule


def create_or_update_schedule_for_day(day_of_week, start_time, end_time, slot_duration, max_bookings_per_slot):
    existing_schedule = Schedule.objects.filter(day_of_week=day_of_week).first()

    if existing_schedule:
        existing_schedule.start_time = start_time
        existing_schedule.end_time = end_time
        existing_schedule.slot_duration = slot_duration
        existing_schedule.max_bookings_per_slot = max_bookings_per_slot
        existing_schedule.save()
        print(f"Updated schedule for {day_of_week}")
    else:
        Schedule.objects.create(
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            slot_duration=slot_duration,
            max_bookings_per_slot=max_bookings_per_slot
        )
        print(f"Created schedule for {day_of_week}")


def populate_week_schedule(start_hour=9, end_hour=17, slot_duration_minutes=30, max_bookings_per_slot=1):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    slot_duration = timedelta(minutes=slot_duration_minutes)  # Convert slot duration to timedelta
    start_time = time(start_hour, 0)
    end_time = time(end_hour, 0)

    for day_of_week in weekdays:
        create_or_update_schedule_for_day(day_of_week, start_time, end_time, slot_duration, max_bookings_per_slot)


if __name__ == "__main__":
    populate_week_schedule()