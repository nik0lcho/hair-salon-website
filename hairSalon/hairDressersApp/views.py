from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import TimeSlot, AvailableDate, Schedule


def get_available_dates(request):
    """
    Fetch all available dates for selection.
    """
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        available_dates = AvailableDate.objects.values('id', 'date')
        return JsonResponse({
            'available_dates': [{'id': date_obj['id'], 'display': date_obj['date'].strftime("%Y-%m-%d")} for date_obj in available_dates]
        })
    return JsonResponse({"error": "Invalid request"}, status=400)


def get_timeslots(request):
    """
    Fetch all available time slots for a selected date.
    """
    date_id = request.GET.get('date')
    try:
        if not date_id:
            raise ValueError("Date ID is required.")

        timeslots = TimeSlot.objects.filter(is_available=True, date_id=date_id,)

        return JsonResponse({
            'time_slots': [{'id': ts.id, 'display': str(ts)} for ts in timeslots]
        })
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
