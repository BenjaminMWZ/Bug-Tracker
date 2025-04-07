# Bug Tracker

A Django and React application for tracking bugs reported via email.

## Overview

This Bug Tracker application allows users to:

1. Receive bug reports via email
2. Automatically parse emails to create or update bug records
3. View a list of all bugs with filtering and sorting options
4. See detailed information about each bug
5. Visualize bug modification activity over time through a dashboard

## Features

### Backend (Django)

- **Email Processing**: Automatically processes incoming emails to create or update bug records
- **Celery Integration**: Uses Celery for asynchronous email processing
- **RESTful API**: Provides endpoints for accessing bug data
- **Authentication**: JWT-based authentication system
- **Database**: SQLite for development (configurable for other databases in production)

### Frontend (React)

- **Bug List**: Tabular view of all bugs with sorting and filtering
- **Bug Details**: Detailed view of each bug with all relevant information
- **Dashboard**: Visualization of bug modifications over time
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**:
  - Django 4.2
  - Django REST Framework
  - Celery for asynchronous tasks
  - SQLite (development) 

- **Frontend**:
  - React 18
  - Ant Design for UI components
  - Recharts for data visualization
  - React Router for navigation

## Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Bug-Tracker.git
   cd Bug-Tracker

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ``` 
Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd web
   ```
2. Install frontend dependencies:
   ```bash
    npm install
    ```
3. Start the frontend development server:
    ```bash
    npm start
    ```
Run the Celery worker:
1. Start the Celery worker in a separate terminal:
```bash
celery -A bug_tracker worker --loglevel=info
```
2. Start the Celery beat scheduler in another terminal:
```bash
celery -A bug_tracker beat --loglevel=info
``` 
3. Alternatively, you can run combined development command:
```bash
python manage.py runserver_with_celery
```

## Usage
### Email Processing 
The system will automatically process emails sent to the configured email address. Emails should follow this format:
```
Subject: Bug Report - [Bug Title]
Body:
[Bug Description]
```
If the bug ID already exists, the system updates the existing bug record. Otherwise, it creates a new bug record.

### Example email:
```
Subject: Bug ID: BUG-1234 - Login page not working
Body: Users are reporting that they cannot log in to the application. The login button seems unresponsive.
```

### Status and Priority
The system can detect status and priority information from email content:

Status can be extracted from phrases like "Status: resolved" or "The bug is now closed"
Priority can be detected from words like "URGENT", "CRITICAL", or explicit "Priority: High" mentions

## Web Interface
Bug List: Navigate to /bugs to see all bugs
Bug Details: Click on a bug ID to see detailed information
Dashboard: Navigate to /dashboard to see bug modification statistics

## Testing
Run the backend tests:
```bash
python manage.py test
```
Run the frontend tests:
```bash
npm test
```

## Authenticataion
The API uses JWT authentication. To access protected endpoints:

Obtain a token by sending a POST request to /api/auth/login/ with valid credentials
Include the token in the Authorization header: Authorization: Token <your-token>

## File Structure
```
Bug-Tracker/
├── server/                 # Django backend
│   ├── issues/             # Main app for bug tracking
│   │   ├── management/     # Custom management commands
│   │   │   └── commands/   # Contains process_emails command
│   │   ├── migrations/     # Database migrations
│   │   ├── models.py       # Data models
│   │   ├── serializers.py  # API serializers
│   │   ├── tasks.py        # Celery tasks
│   │   ├── tests.py        # Unit tests
│   │   └── views.py        # API views
│   └── server/             # Project settings
├── web/                    # React frontend
│   ├── public/             # Static files
│   └── src/                # Source code
│       ├── components/     # React components
│       ├── api/            # API client code
│       ├── context/        # React context providers
│       └── utils/          # Utility functions
└── requirements.txt        # Python dependencies
```

## Author
Weizhe Mao
