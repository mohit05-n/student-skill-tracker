# Student Skills Portal

## Overview

The Student Skills Portal is a Flask-based web application that provides a comprehensive platform for managing student profiles, tracking skills, and monitoring certifications. The application features user authentication, student management, skills tracking organized by courses, and certification management.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with support for both SQLite (development) and PostgreSQL (production)
- **Authentication**: Flask-Login for session management
- **Forms**: Flask-WTF with WTForms for form handling and validation
- **Server**: Gunicorn WSGI server for production deployment

### Frontend Architecture
- **Templates**: Jinja2 templating engine
- **CSS Framework**: Bootstrap 5 with dark theme
- **Icons**: Font Awesome 6.0
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### Database Architecture
- **ORM**: SQLAlchemy with declarative base
- **Primary Models**: Student, Skill, Certification
- **Relationships**: Many-to-many relationship between Students and Skills
- **Connection Management**: Pool recycling and pre-ping for connection health

## Key Components

### Models (models.py)
- **Student**: User model with Flask-Login integration, password hashing, and relationships
- **Skill**: Skills categorized by course with many-to-many relationship to students
- **Certification**: Individual certifications linked to students with issue/expiry dates
- **Association Table**: student_skills for many-to-many Student-Skill relationship

### Forms (forms.py)
- **LoginForm**: User authentication with remember me option
- **RegistrationForm**: New user registration with validation
- **StudentForm**: Admin form for adding students with skill selection
- **EditProfileForm**: User profile editing capabilities
- **CertificationForm**: Adding certifications with date validation

### Routes (routes.py)
- **Authentication Routes**: Login, registration, logout
- **Dashboard**: Overview with statistics and quick actions
- **Student Management**: CRUD operations for student profiles
- **Skills Management**: Skills organized by course view
- **Profile Management**: User profile editing and certification addition

### Templates
- **Base Template**: Consistent navigation and styling across all pages
- **Authentication Pages**: Login and registration forms
- **Dashboard**: Statistics cards and management overview
- **Profile Pages**: User profile display and editing
- **Student Management**: List view and individual student details

## Data Flow

1. **User Authentication**: Users register/login through Flask-Login system
2. **Session Management**: User sessions maintained with secure session cookies
3. **Database Operations**: SQLAlchemy handles all database interactions with automatic connection pooling
4. **Form Processing**: Flask-WTF validates and processes all user input
5. **Template Rendering**: Jinja2 renders dynamic content with context data

## External Dependencies

### Python Packages
- **Flask**: Core web framework
- **Flask-SQLAlchemy**: Database ORM integration
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation and rendering
- **Werkzeug**: WSGI utilities and password hashing
- **Gunicorn**: Production WSGI server
- **psycopg2-binary**: PostgreSQL adapter
- **email-validator**: Email validation for forms

### Frontend Libraries
- **Bootstrap 5**: CSS framework with dark theme
- **Font Awesome 6**: Icon library
- **Bootstrap Agent Dark Theme**: Replit-specific styling

## Deployment Strategy

### Development Environment
- **Database**: SQLite for local development
- **Server**: Flask development server with debug mode
- **Environment**: Python 3.11 with Nix package management

### Production Environment
- **Database**: PostgreSQL with connection pooling
- **Server**: Gunicorn with autoscale deployment
- **Security**: ProxyFix middleware for proper header handling
- **Environment Variables**: DATABASE_URL and SESSION_SECRET configuration

### Configuration Management
- **Environment-based**: Different settings for development/production
- **Database URI**: Configurable via DATABASE_URL environment variable
- **Secret Key**: Configurable via SESSION_SECRET environment variable
- **Connection Pool**: Configured for production reliability

## Recent Changes
- June 23, 2025: Fixed all import errors for VS Code compatibility
- June 23, 2025: Created VS Code-compatible files with absolute imports only
- June 23, 2025: Simplified dependencies (removed PostgreSQL for local development)
- June 23, 2025: Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.