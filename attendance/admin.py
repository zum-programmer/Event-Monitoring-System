from django.contrib import admin
from .models import Attendance, Attendee, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "date", "start_time", "end_time")
    search_fields = ("name", "location")
    list_filter = ("date",)


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = (
        "number_id",
        "first_name",
        "last_name",
        "course",
        "year_level",
    )
    search_fields = (
        "number_id",
        "first_name",
        "last_name",
        "course",
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "attendee",
        "check_in",
        "check_out",
        "status",
    )
    list_filter = ("status", "event")
    search_fields = (
        "attendee__number_id",
        "attendee__first_name",
        "attendee__last_name",
    )
