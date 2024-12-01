from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from hairSalon.hairDressersApp.models import TimeSlot
from hairSalon.usersApp.models import Appointment


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()  # Dynamically get the user model
        fields = ('email', 'first_name', 'last_name')


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['client', 'service', 'schedule', 'time_slots']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'schedule' in self.data:
            try:
                schedule_id = int(self.data.get('schedule'))
                self.fields['time_slots'].queryset = TimeSlot.objects.filter(
                    schedule_id=schedule_id, is_available=True
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['time_slots'].queryset = self.instance.schedule.time_slots.filter(is_available=True)
        else:
            self.fields['time_slots'].queryset = TimeSlot.objects.none()
