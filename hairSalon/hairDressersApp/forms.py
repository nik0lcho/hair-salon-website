from django import forms
from .models import Appointment, AvailableDate, TimeSlot


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time_slots']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.Select(attrs={'class': 'form-control'}),
            'time_slots': forms.Select(attrs={'class': 'form-control'}),
        }
