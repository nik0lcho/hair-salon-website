from django.contrib import admin
from .models import AppUser, Profile, Review, Appointment


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
    list_display = ('client', 'appointment_date')
    search_fields = ('client__email', 'service__name')
    list_filter = ['service__name']
    ordering = ['appointment_date']
