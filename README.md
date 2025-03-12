# Task Management System

This is a Task Management System built with Django, providing APIs for user authentication, task management, and real-time notifications using WebSocket and Web Push notifications. The system allows users to register, login, assign tasks, and complete them with real-time updates and notifications.

## Features

- **User Authentication:**
  - User Registration
  - Login
  - Logout
  - Token-based authentication (Refresh tokens included)

- **Task Management:**
  - Create a task
  - Update a task
  - Delete a task
  - Mark a task as complete

- **Task Search:**
  - Search tasks based on different filters

- **Real-Time Notifications:**
  - WebSocket integration for real-time task updates
  - Web Push notifications for task creation and completion

## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- Django REST Framework
- Channels (for WebSocket support)
- Django WebPush (for push notifications)

### Steps to Install

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
  python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

-add database of postgress or mysql in settings.py than migrate

python manage.py migrate
python manage.py runserver


Now you can access all the url


