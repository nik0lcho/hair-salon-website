from .forms import AppUserCreationForm, AppUserChangeForm
from .models import Review

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active',)
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    add_form = AppUserCreationForm  # Custom creation form
    form = AppUserChangeForm

    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'first_name', 'last_name', 'is_active',)}
         ),
    )
    filter_horizontal = ()


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at', 'approved')
    list_filter = ('rating', 'approved')
    search_fields = ['user__email']
    fields = ('user', 'rating', 'content', 'approved')
    ordering = ['-created_at']
