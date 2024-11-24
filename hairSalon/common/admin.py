from django.contrib import admin
from .models import Service

# Register your models here.


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')
    list_filter = ('price', 'duration')
    search_fields = ['name']
    ordering = ['name']
