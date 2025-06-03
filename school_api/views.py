from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Subject, Class, Student, AttendanceRecord, Announcement
from .serializers import (
    UserSerializer, UserUpdateSerializer, ChangePasswordSerializer,
    SubjectSerializer, ClassSerializer, StudentSerializer, EnrollStudentsSerializer,
    AttendanceRecordSerializer, AnnouncementSerializer
)
from .permissions import (
    IsAdministrator, IsTeacher, IsStudent, IsParent,
    IsOwnerOrAdministrator, IsTeacherOrAdministrator, IsStudentOrTeacherOrAdministrator
)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'email', 'first_name', 'last_name', 'role', 'created_at']

    def get_permissions(self):
        if self.action == 'create':
            # Allow anyone to register (for initial setup)
            return [AllowAny()]
        elif self.action == 'change_password':
            # Allow authenticated users to change their own password
            return [IsAuthenticated()]
        else:
            # Only administrators can perform other actions on users
            return [IsAdministrator()]

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return UserUpdateSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        user = self.get_object()

        # Only administrators or the user themselves can change their password
        if request.user.role != 'Administrator' and request.user.id != user.id:
            return Response(
                {"detail": "You do not have permission to change this user's password."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"status": "password set"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for subjects
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Anyone authenticated can view subjects
            return [IsAuthenticated()]
        else:
            # Only administrators can create, update, or delete subjects
            return [IsAdministrator()]

class ClassViewSet(viewsets.ModelViewSet):
    """
    API endpoint for classes
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'academic_year', 'location', 'teacher__first_name', 'teacher__last_name', 'subject__name']
    ordering_fields = ['name', 'academic_year', 'scheduled_start_time', 'scheduled_end_time', 'location', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Anyone authenticated can view classes
            return [IsAuthenticated()]
        elif self.action == 'enroll_students':
            # Only teachers of the class or administrators can enroll students
            return [IsTeacherOrAdministrator()]
        else:
            # Only administrators can create, update, or delete classes
            return [IsAdministrator()]

    def perform_create(self, serializer):
        # Ensure the teacher has the Teacher role
        teacher = serializer.validated_data.get('teacher')
        if teacher.role != 'Teacher':
            raise serializers.ValidationError({"teacher": "Selected user is not a teacher."})
        serializer.save()

    @action(detail=True, methods=['post'])
    def enroll_students(self, request, pk=None):
        class_obj = self.get_object()

        # Check if the user is the teacher of this class or an administrator
        if request.user.role != 'Administrator' and request.user != class_obj.teacher:
            return Response(
                {"detail": "You do not have permission to enroll students in this class."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = EnrollStudentsSerializer(data=request.data)
        if serializer.is_valid():
            student_ids = serializer.validated_data['student_ids']
            students = Student.objects.filter(id__in=student_ids)

            # Check if all student IDs are valid
            if len(students) != len(student_ids):
                return Response(
                    {"student_ids": "Some student IDs are invalid."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Enroll students
            for student in students:
                class_obj.enrolled_students.add(student)

            return Response({"status": "students enrolled"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for students
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['roll_number', 'user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['roll_number', 'user__first_name', 'user__last_name', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Teachers, administrators, and the student themselves can view student details
            return [IsStudentOrTeacherOrAdministrator()]
        else:
            # Only administrators can create, update, or delete students
            return [IsAdministrator()]

    def perform_create(self, serializer):
        # Ensure the user has the Student role
        user = serializer.validated_data.get('user')
        if user.role != 'Student':
            raise serializers.ValidationError({"user": "Selected user is not a student."})
        serializer.save()

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint for attendance records
    """
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__roll_number', 'student__user__first_name', 'student__user__last_name', 'class_obj__name']
    ordering_fields = ['attendance_date', 'attendance_time', 'status', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Anyone authenticated can view attendance records
            return [IsAuthenticated()]
        else:
            # Only teachers or administrators can create, update, or delete attendance records
            return [IsTeacherOrAdministrator()]

    def perform_create(self, serializer):
        # Set the recorded_by field to the current user
        serializer.save(recorded_by=self.request.user)

    @action(detail=False, methods=['get'])
    def student_history(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {"detail": "Student ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        student = get_object_or_404(Student, id=student_id)

        # Check if the user is the student, a teacher of one of their classes, or an administrator
        if (request.user.role != 'Administrator' and 
            request.user.role != 'Teacher' and 
            (request.user.role != 'Student' or request.user != student.user)):
            return Response(
                {"detail": "You do not have permission to view this student's attendance history."},
                status=status.HTTP_403_FORBIDDEN
            )

        attendance_records = AttendanceRecord.objects.filter(student=student).order_by('-attendance_date')
        serializer = self.get_serializer(attendance_records, many=True)
        return Response(serializer.data)

class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for announcements
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'message', 'type', 'audience']
    ordering_fields = ['title', 'type', 'audience', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Anyone authenticated can view announcements
            return [IsAuthenticated()]
        else:
            # Only teachers or administrators can create, update, or delete announcements
            return [IsTeacherOrAdministrator()]

    def perform_create(self, serializer):
        # Set the created_by field to the current user
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        """
        Filter announcements based on user role
        """
        queryset = Announcement.objects.all()

        # If the user is not an administrator or teacher, filter announcements by audience
        if self.request.user.role not in ['Administrator', 'Teacher']:
            if self.request.user.role == 'Student':
                queryset = queryset.filter(audience__in=['All', 'Students'])
            elif self.request.user.role == 'Parent':
                queryset = queryset.filter(audience__in=['All', 'Parents'])

        return queryset.order_by('-created_at')
