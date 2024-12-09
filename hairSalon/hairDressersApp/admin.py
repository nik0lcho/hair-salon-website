from django.contrib import admin
from .models import Schedule, TimeSlot, Appointment


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'day_of_week', 'start_time', 'end_time',)
    list_filter = ('day_of_week',)
    search_fields = ('day_of_week',)
    actions = ['activate_schedules', 'deactivate_schedules']

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Staff').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'is_available')
    list_filter = ('date', 'is_available',)
    search_fields = ('date',)
    ordering = ('date', 'start_time')

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Staff').exists()

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['date', 'start_time']  # Non-superusers can only view these
        return super().get_readonly_fields(request, obj)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'date', 'time_slots')
    list_filter = ('service',)

    class Media:
        js = ('admin/js/fetchAvailableDates.js',
              'admin/js/fetchTimeSlots.js')

    actions = ['free_appointment',]

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Staff').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False

    def free_appointment(modeladmin, request, queryset):
        # Iterate through all selected appointments
        for appointment in queryset:
            # Get the associated time slot
            time_slots = appointment.time_slots

            # Mark the time slot as available
            time_slots.is_available = True
            time_slots.save()

            # Delete the appointment
            appointment.delete()

        # You can show a success message once the action is completed
        modeladmin.message_user(request, "Selected appointments have been freed and timeslots made available.")

    free_appointment.short_description = "Free appointments"

    def get_actions(self, request):
        # Remove the delete action
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
