from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("add-event/", views.add_event, name="add_event"),
    path("enroll-student/", views.enroll_student, name="enroll_student"),
    path("check-number-id/", views.check_number_id, name="check_number_id"),
]
