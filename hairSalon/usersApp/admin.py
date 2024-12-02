from django import forms
from django.contrib import admin
from django.http import JsonResponse

from .models import AppUser, Profile, Review, Appointment, TimeSlot


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')
    search_fields = ('user__email', 'first_name', 'last_name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at', 'approved')
    list_filter = ('rating', 'approved')
    search_fields = ['user__email']
    fields = ('user', 'rating', 'content', 'approved')

    ordering = ['-created_at']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'date', 'time_slots')
    list_filter = ('service',)
    search_fields = ('client__email',)

    class Media:
        js = ('admin/js/schedule_timeslot_filter.js',)

    def changelist_view(self, request, extra_context=None):
        # Check if the request is an AJAX request and contains the 'date' parameter
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'date' in request.GET:
            selected_date = request.GET['date']

            # Filter TimeSlots by the selected date
            time_slots = TimeSlot.objects.filter(date=selected_date, is_available=True)

            # Return the time slots as a JSON response
            return JsonResponse({
                'time_slots': [{'id': ts.id, 'display': str(ts)} for ts in time_slots]
            })

        # Call the parent class' changelist_view for normal handling
        return super().changelist_view(request, extra_context=extra_context)
