# Classroom Management System

## Description
The Classroom Management System is a software application designed to streamline and automate various administrative tasks related to managing classrooms in a college setting. It provides a centralized platform for teachers, students, and administrators to efficiently manage class schedules, attendance, assignments, grades, and communication.

## Features
- User-friendly interface for easy navigation and usage
- Secure authentication and access control for different user roles
- Class scheduling and timetable management
- Attendance tracking and reporting
- Gradebook management and progress tracking
- Communication tools for teachers and students (announcements, notifications)
- Reporting and analytics for administrators

## Usage
1. Access the application through your web browser
2. Sign in with your credentials (Hod, Faculity, or student)
3. Explore the different features and functionalities available
4. Perform administrative tasks (if applicable)
5. Manage classes, attendance, assignments, and grades
6. Communicate with teachers and students
7. Generate reports and analyze data


# Requirements

To set up the project, you will need to install the dependencies listed in the `req.txt` file. You can do this by running the following command:

```bash 
pip install -r req.txt

sudo apt install rabbitmq-server
```

To generate Tailwind CSS, run the following command:

```bash
 npx tailwindcss -i input.css -o ./Home/static/public/css/base.css --watch
```


# Running the Application

To run the application, you will need to start the Django development server by running the following command:

```bash
python manage.py runserver
```

You will also need to start the Celery worker and beat processes by running the following commands:

```bash
celery -A IgCMS worker

celery -A IgCMS beat
```
