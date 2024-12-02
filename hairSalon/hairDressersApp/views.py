from django.http import JsonResponse
from datetime import datetime
from .models import TimeSlot


def get_timeslots(request):
    date_str = request.GET.get('date')
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        timeslots = TimeSlot.objects.filter(date=target_date, is_available=True)

        return JsonResponse({
            'time_slots': [{'id': ts.id, 'display': str(ts)} for ts in timeslots]
        })
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
