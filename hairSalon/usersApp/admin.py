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
        js = 'admin/js/appointment_logic.js'
