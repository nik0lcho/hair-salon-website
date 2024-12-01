# Create your views here.
from django.http import JsonResponse
from .models import TimeSlot


def get_timeslots(request):
    schedule_id = request.GET.get('schedule_id')
    date = request.GET.get('date')  # Optional specific date

    if schedule_id:
        timeslots = TimeSlot.objects.filter(schedule_id=schedule_id, is_available=True)

        if date:
            timeslots = timeslots.filter(date=date)

        data = [
            {
                'id': slot.id,
                'label': f"{slot.start_time.strftime('%H:%M')} - {'Available' if slot.is_available else 'Booked'}"
            }
            for slot in timeslots
        ]
        return JsonResponse(data, safe=False)

    return JsonResponse([], safe=False)
