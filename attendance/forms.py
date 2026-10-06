from django import forms

from .models import Attendee, Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "location",
            "date",
            "start_time",
            "end_time",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Enter event name",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Enter event description",
                "rows": 4,
            }),
            "location": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Enter event location",
            }),
            "date": forms.DateInput(attrs={
                "class": "form-input",
                "type": "date",
            }),
            "start_time": forms.TimeInput(attrs={
                "class": "form-input",
                "type": "time",
            }),
            "end_time": forms.TimeInput(attrs={
                "class": "form-input",
                "type": "time",
            }),
        }


class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = [
            "number_id",
            "first_name",
            "last_name",
            "email",
            "course",
            "year_level",
        ]
        widgets = {
            "number_id": forms.TextInput(attrs={
                "class": "form-input id-field",
                "placeholder": "e.g. 2026-0001",
                "autocomplete": "off",
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "First name",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Last name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input",
                "placeholder": "student@example.com",
            }),
            "course": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. BS Information Technology",
            }),
            "year_level": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. 1st Year",
            }),
        }
