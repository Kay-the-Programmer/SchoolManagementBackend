import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from school_api.models import Subject, Class, Student, AttendanceRecord, Announcement

User = get_user_model()

class Command(BaseCommand):
    help = 'Loads initial data for the school management system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading initial data...')
        
        # Create users with different roles
        self.create_users()
        
        # Create subjects
        self.create_subjects()
        
        # Create classes
        self.create_classes()
        
        # Create students and enroll them in classes
        self.create_students()
        
        # Create attendance records
        self.create_attendance_records()
        
        # Create announcements
        self.create_announcements()
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data!'))
    
    def create_users(self):
        # Create administrator
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@school.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'Administrator',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created administrator: {admin_user.username}')
        
        # Create teachers
        teachers_data = [
            {
                'username': 'teacher1',
                'email': 'teacher1@school.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'role': 'Teacher',
                'password': 'teacher123'
            },
            {
                'username': 'teacher2',
                'email': 'teacher2@school.com',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'role': 'Teacher',
                'password': 'teacher123'
            },
        ]
        
        for teacher_data in teachers_data:
            password = teacher_data.pop('password')
            teacher, created = User.objects.get_or_create(
                username=teacher_data['username'],
                defaults=teacher_data
            )
            if created:
                teacher.set_password(password)
                teacher.save()
                self.stdout.write(f'Created teacher: {teacher.username}')
        
        # Create students
        students_data = [
            {
                'username': 'student1',
                'email': 'student1@school.com',
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'role': 'Student',
                'password': 'student123'
            },
            {
                'username': 'student2',
                'email': 'student2@school.com',
                'first_name': 'Bob',
                'last_name': 'Brown',
                'role': 'Student',
                'password': 'student123'
            },
            {
                'username': 'student3',
                'email': 'student3@school.com',
                'first_name': 'Charlie',
                'last_name': 'Davis',
                'role': 'Student',
                'password': 'student123'
            },
        ]
        
        for student_data in students_data:
            password = student_data.pop('password')
            student, created = User.objects.get_or_create(
                username=student_data['username'],
                defaults=student_data
            )
            if created:
                student.set_password(password)
                student.save()
                self.stdout.write(f'Created student: {student.username}')
        
        # Create parents
        parents_data = [
            {
                'username': 'parent1',
                'email': 'parent1@school.com',
                'first_name': 'David',
                'last_name': 'Johnson',
                'role': 'Parent',
                'password': 'parent123'
            },
            {
                'username': 'parent2',
                'email': 'parent2@school.com',
                'first_name': 'Emily',
                'last_name': 'Brown',
                'role': 'Parent',
                'password': 'parent123'
            },
        ]
        
        for parent_data in parents_data:
            password = parent_data.pop('password')
            parent, created = User.objects.get_or_create(
                username=parent_data['username'],
                defaults=parent_data
            )
            if created:
                parent.set_password(password)
                parent.save()
                self.stdout.write(f'Created parent: {parent.username}')
    
    def create_subjects(self):
        subjects_data = [
            {'name': 'Mathematics'},
            {'name': 'Science'},
            {'name': 'English'},
            {'name': 'History'},
            {'name': 'Computer Science'},
        ]
        
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(**subject_data)
            if created:
                self.stdout.write(f'Created subject: {subject.name}')
    
    def create_classes(self):
        # Get teachers
        teacher1 = User.objects.get(username='teacher1')
        teacher2 = User.objects.get(username='teacher2')
        
        # Get subjects
        math = Subject.objects.get(name='Mathematics')
        science = Subject.objects.get(name='Science')
        english = Subject.objects.get(name='English')
        history = Subject.objects.get(name='History')
        cs = Subject.objects.get(name='Computer Science')
        
        classes_data = [
            {
                'name': 'Math 101',
                'academic_year': '2023-2024',
                'scheduled_start_time': '09:00:00',
                'scheduled_end_time': '10:30:00',
                'days_of_week': 'Monday,Wednesday,Friday',
                'location': 'Room 101',
                'teacher': teacher1,
                'subject': math,
            },
            {
                'name': 'Science 101',
                'academic_year': '2023-2024',
                'scheduled_start_time': '11:00:00',
                'scheduled_end_time': '12:30:00',
                'days_of_week': 'Tuesday,Thursday',
                'location': 'Lab 201',
                'teacher': teacher2,
                'subject': science,
            },
            {
                'name': 'English 101',
                'academic_year': '2023-2024',
                'scheduled_start_time': '13:00:00',
                'scheduled_end_time': '14:30:00',
                'days_of_week': 'Monday,Wednesday',
                'location': 'Room 102',
                'teacher': teacher1,
                'subject': english,
            },
            {
                'name': 'History 101',
                'academic_year': '2023-2024',
                'scheduled_start_time': '15:00:00',
                'scheduled_end_time': '16:30:00',
                'days_of_week': 'Tuesday,Thursday',
                'location': 'Room 103',
                'teacher': teacher2,
                'subject': history,
            },
            {
                'name': 'Computer Science 101',
                'academic_year': '2023-2024',
                'scheduled_start_time': '09:00:00',
                'scheduled_end_time': '10:30:00',
                'days_of_week': 'Tuesday,Thursday',
                'location': 'Lab 202',
                'teacher': teacher1,
                'subject': cs,
            },
        ]
        
        for class_data in classes_data:
            class_obj, created = Class.objects.get_or_create(
                name=class_data['name'],
                defaults=class_data
            )
            if created:
                self.stdout.write(f'Created class: {class_obj.name}')
    
    def create_students(self):
        # Get student users
        student1_user = User.objects.get(username='student1')
        student2_user = User.objects.get(username='student2')
        student3_user = User.objects.get(username='student3')
        
        # Get classes
        math_class = Class.objects.get(name='Math 101')
        science_class = Class.objects.get(name='Science 101')
        english_class = Class.objects.get(name='English 101')
        history_class = Class.objects.get(name='History 101')
        cs_class = Class.objects.get(name='Computer Science 101')
        
        # Create students
        student1, created = Student.objects.get_or_create(
            user=student1_user,
            defaults={'roll_number': 'S001'}
        )
        if created:
            student1.classes.add(math_class, science_class, english_class)
            self.stdout.write(f'Created student: {student1.user.first_name} {student1.user.last_name}')
        
        student2, created = Student.objects.get_or_create(
            user=student2_user,
            defaults={'roll_number': 'S002'}
        )
        if created:
            student2.classes.add(math_class, history_class, cs_class)
            self.stdout.write(f'Created student: {student2.user.first_name} {student2.user.last_name}')
        
        student3, created = Student.objects.get_or_create(
            user=student3_user,
            defaults={'roll_number': 'S003'}
        )
        if created:
            student3.classes.add(science_class, english_class, cs_class)
            self.stdout.write(f'Created student: {student3.user.first_name} {student3.user.last_name}')
    
    def create_attendance_records(self):
        # Get students
        student1 = Student.objects.get(roll_number='S001')
        student2 = Student.objects.get(roll_number='S002')
        student3 = Student.objects.get(roll_number='S003')
        
        # Get classes
        math_class = Class.objects.get(name='Math 101')
        science_class = Class.objects.get(name='Science 101')
        english_class = Class.objects.get(name='English 101')
        
        # Get teachers
        teacher1 = User.objects.get(username='teacher1')
        teacher2 = User.objects.get(username='teacher2')
        
        # Create attendance records
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        day_before = today - datetime.timedelta(days=2)
        
        attendance_records_data = [
            {
                'student': student1,
                'class_obj': math_class,
                'attendance_date': today,
                'attendance_time': '09:00:00',
                'status': 'Present',
                'checkin_method': 'QR_STATIC',
                'recorded_by': teacher1,
            },
            {
                'student': student1,
                'class_obj': science_class,
                'attendance_date': today,
                'attendance_time': '11:00:00',
                'status': 'Present',
                'checkin_method': 'QR_STATIC',
                'recorded_by': teacher2,
            },
            {
                'student': student1,
                'class_obj': math_class,
                'attendance_date': yesterday,
                'attendance_time': '09:00:00',
                'status': 'Late',
                'notes': 'Arrived 10 minutes late',
                'checkin_method': 'MANUAL',
                'recorded_by': teacher1,
            },
            {
                'student': student2,
                'class_obj': math_class,
                'attendance_date': today,
                'attendance_time': '09:00:00',
                'status': 'Present',
                'checkin_method': 'QR_STATIC',
                'recorded_by': teacher1,
            },
            {
                'student': student2,
                'class_obj': math_class,
                'attendance_date': yesterday,
                'attendance_time': '09:00:00',
                'status': 'Absent',
                'notes': 'No notification received',
                'checkin_method': 'MANUAL',
                'recorded_by': teacher1,
            },
            {
                'student': student3,
                'class_obj': science_class,
                'attendance_date': today,
                'attendance_time': '11:00:00',
                'status': 'Present',
                'checkin_method': 'QR_STATIC',
                'recorded_by': teacher2,
            },
            {
                'student': student3,
                'class_obj': english_class,
                'attendance_date': day_before,
                'attendance_time': '13:00:00',
                'status': 'Excused',
                'notes': 'Medical appointment',
                'checkin_method': 'MANUAL',
                'recorded_by': teacher1,
            },
        ]
        
        for record_data in attendance_records_data:
            try:
                record, created = AttendanceRecord.objects.get_or_create(
                    student=record_data['student'],
                    class_obj=record_data['class_obj'],
                    attendance_date=record_data['attendance_date'],
                    defaults=record_data
                )
                if created:
                    self.stdout.write(f'Created attendance record: {record.student} - {record.class_obj.name} - {record.attendance_date}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating attendance record: {e}'))
    
    def create_announcements(self):
        # Get users
        admin = User.objects.get(username='admin')
        teacher1 = User.objects.get(username='teacher1')
        
        announcements_data = [
            {
                'title': 'Welcome to the New School Year',
                'message': 'Welcome to the 2023-2024 academic year! We are excited to have you all back.',
                'type': 'General',
                'audience': 'All',
                'created_by': admin,
            },
            {
                'title': 'Math Test Next Week',
                'message': 'There will be a math test next Monday. Please prepare chapters 1-3.',
                'type': 'Event',
                'audience': 'Students',
                'created_by': teacher1,
            },
            {
                'title': 'Parent-Teacher Meeting',
                'message': 'Parent-teacher meetings will be held next Thursday from 4 PM to 7 PM.',
                'type': 'Event',
                'audience': 'Parents',
                'created_by': admin,
            },
            {
                'title': 'School Closed for Holiday',
                'message': 'The school will be closed next Friday for the national holiday.',
                'type': 'Holiday',
                'audience': 'All',
                'created_by': admin,
            },
            {
                'title': 'Urgent: Fire Drill Tomorrow',
                'message': 'There will be a fire drill tomorrow at 10 AM. Please follow the evacuation procedures.',
                'type': 'Urgent',
                'audience': 'All',
                'created_by': admin,
            },
        ]
        
        for announcement_data in announcements_data:
            announcement, created = Announcement.objects.get_or_create(
                title=announcement_data['title'],
                defaults=announcement_data
            )
            if created:
                self.stdout.write(f'Created announcement: {announcement.title}')