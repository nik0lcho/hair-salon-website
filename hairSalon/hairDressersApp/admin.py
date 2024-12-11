from django.contrib import admin
from .models import Schedule, TimeSlot, Appointment


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'day_of_week', 'start_time', 'end_time',)
    list_filter = ('day_of_week',)
    search_fields = ('day_of_week',)
    actions = ['activate_schedules', 'deactivate_schedules']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'is_available')
    list_filter = ('date', 'is_available',)
    search_fields = ('date',)
    ordering = ('date', 'start_time')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'date', 'time_slots')
    list_filter = ('service',)

    class Media:
        js = ('admin/js/fetchAvailableDates.js',
              'admin/js/fetchTimeSlots.js')

    actions = ['free_appointment',]

    def free_appointment(modeladmin, request, queryset):
        for appointment in queryset:
            time_slots = appointment.time_slots

            time_slots.is_available = True
            time_slots.save()

            appointment.delete()

        modeladmin.message_user(request, "Selected appointments have been freed and timeslots made available.")

    free_appointment.short_description = "Free appointments"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
