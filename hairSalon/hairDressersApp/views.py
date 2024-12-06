from django.http import JsonResponse
from .models import TimeSlot, AvailableDate


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

        timeslots = TimeSlot.objects.filter(date_id=date_id, is_available=True)

        return JsonResponse({
            'time_slots': [{'id': ts.id, 'display': str(ts)} for ts in timeslots]
        })
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date ID or no time slots available.'}, status=400)