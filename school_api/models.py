import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# User model extending Django's AbstractUser
class User(AbstractUser):
    ROLE_CHOICES = (
        ('Administrator', 'Administrator'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
        ('Parent', 'Parent'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# Subject model
class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Class model
class Class(models.Model):
    DAYS_OF_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=20)
    scheduled_start_time = models.TimeField()
    scheduled_end_time = models.TimeField()
    days_of_week = models.CharField(max_length=100)  # Stored as comma-separated values
    location = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Teacher'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.subject.name} ({self.academic_year})"

# Student model
class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roll_number = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Student'})
    classes = models.ManyToManyField(Class, related_name='enrolled_students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.roll_number})"

# AttendanceRecord model
class AttendanceRecord(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    )

    CHECKIN_METHOD_CHOICES = (
        ('QR_STATIC', 'QR Static'),
        ('MANUAL', 'Manual'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attendance_date = models.DateField()
    attendance_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    checkin_method = models.CharField(max_length=10, choices=CHECKIN_METHOD_CHOICES)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendance_records')
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'class_obj', 'attendance_date')

    def __str__(self):
        return f"{self.student} - {self.class_obj.name} - {self.attendance_date} - {self.status}"

# Announcement model
class Announcement(models.Model):
    TYPE_CHOICES = (
        ('General', 'General'),
        ('Urgent', 'Urgent'),
        ('Event', 'Event'),
        ('Holiday', 'Holiday'),
    )

    AUDIENCE_CHOICES = (
        ('All', 'All'),
        ('Students', 'Students'),
        ('Teachers', 'Teachers'),
        ('Parents', 'Parents'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    audience = models.CharField(max_length=10, choices=AUDIENCE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_type_display()} - {self.get_audience_display()})"
