from django.contrib import admin
from .models import Schedule, TimeSlot, DeactivateTimeSlots


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
    list_display = ('date', 'start_time', 'schedule', 'is_available')
    list_filter = ('date', 'is_available', 'schedule')
    search_fields = ('date', 'schedule__day_of_week')
    ordering = ('date', 'start_time')


@admin.register(DeactivateTimeSlots)
class DeactivateTimeSlotsAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'is_active', 'reason')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ['reason', 'start_date', 'end_date']
