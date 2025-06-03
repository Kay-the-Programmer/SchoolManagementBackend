# School Management System Backend

A robust Django REST Framework (DRF) backend for a school management system. This backend serves an Angular frontend, handling user authentication, data storage, and API endpoints for various school entities.

## Features

- User authentication with JWT tokens
- Role-based access control (Administrator, Teacher, Student, Parent)
- API endpoints for users, classes, subjects, students, attendance records, and announcements
- Filtering, ordering, and pagination for list views
- Initial data loading for testing
- Angular services for frontend integration

## Technical Stack

- **Backend Framework**: Django 5.2.1
- **API Framework**: Django REST Framework (DRF) 3.16.0
- **Database**: SQLite (for development), PostgreSQL (recommended for production)
- **Authentication**: JWT (djangorestframework-simplejwt 5.5.0)
- **CORS**: django-cors-headers 4.7.0

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SchoolManagementBackend
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Load Initial Data

```bash
python manage.py load_initial_data
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at http://localhost:8000/api/

## API Endpoints

### Authentication

- `POST /api/auth/login/`: Obtain JWT token
- `POST /api/auth/refresh/`: Refresh JWT token

### Users

- `GET /api/users/`: List all users (Admin only)
- `POST /api/users/`: Create a new user
- `GET /api/users/{id}/`: Retrieve a user (Admin only)
- `PUT /api/users/{id}/`: Update a user (Admin only)
- `DELETE /api/users/{id}/`: Delete a user (Admin only)
- `POST /api/users/{id}/change_password/`: Change a user's password (Admin or the user themselves)

### Classes

- `GET /api/classes/`: List all classes
- `POST /api/classes/`: Create a new class (Admin only)
- `GET /api/classes/{id}/`: Retrieve a class
- `PUT /api/classes/{id}/`: Update a class (Admin only)
- `DELETE /api/classes/{id}/`: Delete a class (Admin only)
- `POST /api/classes/{id}/enroll_students/`: Enroll students in a class (Admin or the class's teacher)

### Subjects

- `GET /api/subjects/`: List all subjects
- `POST /api/subjects/`: Create a new subject (Admin only)
- `GET /api/subjects/{id}/`: Retrieve a subject
- `PUT /api/subjects/{id}/`: Update a subject (Admin only)
- `DELETE /api/subjects/{id}/`: Delete a subject (Admin only)

### Students

- `GET /api/students/`: List all students (Admin, Teacher)
- `POST /api/students/`: Create a new student (Admin only)
- `GET /api/students/{id}/`: Retrieve a student (Admin, Teacher, or the student themselves)
- `PUT /api/students/{id}/`: Update a student (Admin only)
- `DELETE /api/students/{id}/`: Delete a student (Admin only)

### Attendance Records

- `GET /api/attendance/`: List all attendance records
- `POST /api/attendance/`: Create a new attendance record (Admin or Teacher)
- `GET /api/attendance/{id}/`: Retrieve an attendance record
- `PUT /api/attendance/{id}/`: Update an attendance record (Admin or Teacher)
- `DELETE /api/attendance/{id}/`: Delete an attendance record (Admin or Teacher)
- `GET /api/attendance/student_history/?student_id={id}`: Get attendance history for a student

### Announcements

- `GET /api/announcements/`: List all announcements (filtered by user role)
- `POST /api/announcements/`: Create a new announcement (Admin or Teacher)
- `GET /api/announcements/{id}/`: Retrieve an announcement
- `PUT /api/announcements/{id}/`: Update an announcement (Admin or Teacher)
- `DELETE /api/announcements/{id}/`: Delete an announcement (Admin or Teacher)

## Initial Users

After running the `load_initial_data` command, the following users will be available:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| teacher1 | teacher123 | Teacher |
| teacher2 | teacher123 | Teacher |
| student1 | student123 | Student |
| student2 | student123 | Student |
| student3 | student123 | Student |
| parent1 | parent123 | Parent |
| parent2 | parent123 | Parent |

## Frontend Services

Angular services for interacting with the backend API are available in the `frontend` directory. These services provide a complete interface to all backend endpoints:

- **AuthService**: Handles authentication, token management, and user state
- **UserService**: Manages user operations (CRUD)
- **SubjectService**: Manages subject operations (CRUD)
- **ClassService**: Manages class operations (CRUD) and student enrollment
- **StudentService**: Manages student operations (CRUD)
- **AttendanceService**: Manages attendance records (CRUD) and student history
- **AnnouncementService**: Manages announcements (CRUD)

For more details, see the [Frontend README](frontend/README.md).

## License

This project is licensed under the MIT License - see the LICENSE file for details.#   S c h o o l M a n a g e m e n t B a c k e n d 
 
 
