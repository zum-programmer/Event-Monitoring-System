from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import AttendeeForm, EventForm
from .models import Attendance, Attendee, Event


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")
    else:
        form = AuthenticationForm()

    return render(request, "attendance/login.html", {"form": form})


@login_required
def dashboard(request):
    event = Event.objects.order_by("-date", "-start_time").first()

    if not event:
        return render(
            request,
            "attendance/dashboard.html",
            {"event": None},
        )

    total_registered = Attendee.objects.count()

    total_present = Attendance.objects.filter(
        event=event,
        status="Present",
    ).count()

    total_late = Attendance.objects.filter(
        event=event,
        status="Late",
    ).count()

    total_checked_in = Attendance.objects.filter(
        event=event,
        check_in__isnull=False,
    ).count()

    total_absent = max(total_registered - total_checked_in, 0)

    recent_attendance = (
        Attendance.objects
        .filter(event=event, check_in__isnull=False)
        .select_related("attendee")
        .order_by("-check_in")[:10]
    )

    return render(
        request,
        "attendance/dashboard.html",
        {
            "event": event,
            "total_registered": total_registered,
            "total_present": total_present,
            "total_late": total_late,
            "total_absent": total_absent,
            "recent_attendance": recent_attendance,
        },
    )


@login_required
def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect("dashboard")
    else:
        form = EventForm()

    return render(
        request,
        "attendance/add_event.html",
        {"form": form},
    )


@login_required
def enroll_student(request):
    if request.method == "POST":
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save()
            return redirect("enroll_student")
    else:
        form = AttendeeForm()

    attendees = Attendee.objects.order_by("last_name", "first_name")[:50]

    return render(
        request,
        "attendance/enroll_student.html",
        {
            "form": form,
            "attendees": attendees,
            "total_students": Attendee.objects.count(),
        },
    )


@login_required
def check_number_id(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Invalid request."},
            status=400,
        )

    number_id = request.POST.get("number_id", "").strip()
    event_id = request.POST.get("event_id")

    if not number_id:
        return JsonResponse({
            "success": False,
            "status": "empty",
            "message": "Please enter a Number ID.",
        })

    if not event_id:
        return JsonResponse({
            "success": False,
            "status": "error",
            "message": "No event selected.",
        })

    event = get_object_or_404(Event, id=event_id)

    try:
        attendee = Attendee.objects.get(number_id=number_id)
    except Attendee.DoesNotExist:
        return JsonResponse({
            "success": False,
            "status": "not_found",
            "message": "ID Not Found",
            "number_id": number_id,
        })

    attendance = Attendance.objects.filter(
        event=event,
        attendee=attendee,
    ).first()

    if attendance and attendance.check_in:
        return JsonResponse({
            "success": False,
            "status": "already_checked_in",
            "message": "Already Checked In",
            "attendee": {
                "number_id": attendee.number_id,
                "name": f"{attendee.first_name} {attendee.last_name}",
                "course": attendee.course,
                "year_level": attendee.year_level,
            },
            "check_in": attendance.check_in.strftime("%I:%M:%S %p"),
        })

    now = timezone.now()

    if not attendance:
        attendance = Attendance.objects.create(
            event=event,
            attendee=attendee,
            check_in=now,
            status="Present",
        )
    else:
        attendance.check_in = now
        attendance.status = "Present"
        attendance.save()

    return JsonResponse({
        "success": True,
        "status": "present",
        "message": "Present",
        "attendee": {
            "number_id": attendee.number_id,
            "name": f"{attendee.first_name} {attendee.last_name}",
            "course": attendee.course,
            "year_level": attendee.year_level,
        },
        "check_in": now.strftime("%I:%M:%S %p"),
    })
