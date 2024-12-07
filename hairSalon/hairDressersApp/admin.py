from django.contrib import admin
from .models import Schedule, TimeSlot, Appointment


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'day_of_week', 'start_time', 'end_time', 'is_active')
    list_filter = ('day_of_week', 'is_active')
    search_fields = ('day_of_week',)
    actions = ['activate_schedules', 'deactivate_schedules']

    def activate_schedules(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected schedules have been activated.")
    activate_schedules.short_description = "Activate selected schedules"

    def deactivate_schedules(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected schedules have been deactivated.")
    deactivate_schedules.short_description = "Deactivate selected schedules"


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'is_available')
    list_filter = ('date', 'is_available',)
    search_fields = ('date',)
    ordering = ('date', 'start_time')

    actions = ['free_up_slot', 'book_slot']

    def free_up_slot(self, request, queryset):
        queryset.update(is_available=True)  # Deactivate selected slots
        self.message_user(request, "Selected slots have been freed up.")

    def book_slot(self, request, queryset):
        queryset.update(is_available=False)  # Activate selected slots
        self.message_user(request, "Selected slots have been booked.")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'date', 'time_slots')
    list_filter = ('service',)

    class Media:
        js = ('admin/js/fetchAvailableDates.js',
              'admin/js/fetchTimeSlots.js')
