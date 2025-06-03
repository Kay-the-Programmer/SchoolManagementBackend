from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Subject, Class, Student, AttendanceRecord, Announcement

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class ClassSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Class
        fields = ['id', 'name', 'academic_year', 'scheduled_start_time', 'scheduled_end_time', 
                 'days_of_week', 'location', 'teacher', 'teacher_name', 'subject', 'subject_name', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'teacher_name', 'subject_name']
    
    def get_teacher_name(self, obj):
        return f"{obj.teacher.first_name} {obj.teacher.last_name}"
    
    def get_subject_name(self, obj):
        return obj.subject.name

class StudentSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    classes_details = ClassSerializer(source='classes', many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'roll_number', 'user', 'user_details', 'classes', 'classes_details', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user_details', 'classes_details']

class EnrollStudentsSerializer(serializers.Serializer):
    student_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=True
    )

class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()
    recorded_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AttendanceRecord
        fields = ['id', 'attendance_date', 'attendance_time', 'status', 'notes', 'checkin_method',
                 'student', 'student_name', 'class_obj', 'class_name', 'recorded_by', 'recorded_by_name',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'student_name', 'class_name', 'recorded_by_name']
    
    def get_student_name(self, obj):
        return f"{obj.student.user.first_name} {obj.student.user.last_name}"
    
    def get_class_name(self, obj):
        return obj.class_obj.name
    
    def get_recorded_by_name(self, obj):
        return f"{obj.recorded_by.first_name} {obj.recorded_by.last_name}"

class AnnouncementSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'message', 'type', 'audience', 'created_by', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name']
    
    def get_created_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"