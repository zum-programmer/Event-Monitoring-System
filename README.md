# Event Attendance Monitoring System

A Django-based event attendance monitoring system using Number ID input.

## Features

- Admin login
- Event management
- Attendee management
- Number ID attendance check-in
- AJAX check-in without page refresh
- `PRESENT` result for a new check-in
- `ALREADY CHECKED IN` result for duplicate scans
- `ID NOT FOUND` result for unknown IDs
- Automatic input clearing and refocusing
- Attendance statistics
- Recent attendance table
- Responsive professional dashboard
- Works with keyboard input and many USB barcode scanners

## Requirements

- Python 3.10+
- Django 5.x

## Installation

Open a terminal inside this project folder.

### 1. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create database tables

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create administrator

```bash
python manage.py createsuperuser
```

Follow the prompts.

### 5. Start the server

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/

Admin:

http://127.0.0.1:8000/admin/

## First setup

1. Open `/admin/`.
2. Create an Event.
3. Create Attendees.
4. Return to `/`.
5. The most recent event will appear on the dashboard.
6. Enter an attendee's Number ID.
7. Press Enter or click CHECK ATTENDANCE.

## Attendance behavior

### New attendee

The system displays:

`✓ PRESENT`

and records the check-in time.

### Duplicate attendee

The system displays:

`⚠ ALREADY CHECKED IN`

and does not create another attendance record.

### Unknown ID

The system displays:

`✕ ID NOT FOUND`

and does not create an attendance record.

## Notes

The current dashboard automatically uses the most recent event. For a multi-event production system, add an event selector so staff can choose the active event.

The system currently marks a new check-in as Present. A later enhancement can automatically determine Late based on the event start time.

## Enrollment page

Staff can now enroll students without using Django Admin:

- Open `/enroll-student/` or click **Enroll Student** in the navigation.
- Enter the student's unique Number ID, name, email, course, and year level.
- The student immediately becomes available to the attendance checker.
- Duplicate Number IDs are rejected.

The **Add Event** page is also available from the navigation at `/add-event/`.
