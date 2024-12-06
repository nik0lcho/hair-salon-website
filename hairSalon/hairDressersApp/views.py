from django.http import JsonResponse
from datetime import datetime
from .models import TimeSlot, AvailableDate


def get_timeslots(request):
    date = request.GET.get('date')
    try:
        # Parse the date string into a datetime object
        target_date = datetime.strptime(date, "%Y-%m-%d").date()

        # Find the `AvailableDate` object matching the target date
        available_date = AvailableDate.objects.filter(date=target_date).first()

        if not available_date:
            return JsonResponse({'time_slots': [], 'message': 'No available slots for the selected date.'})

        # Query time slots associated with the found AvailableDate
        timeslots = TimeSlot.objects.filter(date=available_date, is_available=True)

        return JsonResponse({
            'time_slots': [{'id': ts.id, 'display': str(ts)} for ts in timeslots]
        })
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)


def get_available_dates(request):
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        available_dates = AvailableDate.objects.values_list('date', flat=True)
        return JsonResponse({
            'available_dates': [date.strftime("%Y-%m-%d") for date in available_dates]
        })
    return JsonResponse({"error": "Invalid request"}, status=400)
