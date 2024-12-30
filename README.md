# SpamShield

**SpamShield** is a Django-based backend application designed to power a mobile app for identifying spam phone numbers and searching for user profiles by phone number or name. The project adheres to industry best practices for API design, correctness, performance, scalability, and security.

## Features

### User Management
- User registration with phone number, username, and optional email.
- Login and authentication with token-based access.
- Profile management (view and update user profile).

### Spam Management
- Report numbers as spam with categories and optional comments.
- View spam likelihood based on reports: NotSPAM, LikelySPAM, or SPAM.

### Search
- Search users by name or phone number with efficient indexing.
- Supports paginated results for better performance.

### Contacts Management
- Sync bulk contacts, track who added them, and resolve duplicates.
- Update or patch contacts during resynchronization.

### Audit and Logging
- Track spam reports with timestamps and categories for audits.
- Centralized logging for monitoring API requests, responses, and errors.

## Key Design Aspects

### 1. Correctness Under Thorough Testing
- Unit tests are implemented for models, views, and serializers.
- Test cases for edge scenarios like duplicate phone numbers, invalid spam categories, and bulk contact syncs.

### 2. Performance and Scalability
- **Database Indexing**: Critical columns like `phone_number`, `name`, and `reported_at` are indexed to speed up search queries.
- **Pagination**: All search APIs support pagination to reduce data transfer and enhance performance.
- **Optimized Queries**: Carefully designed ORM queries to minimize database load.
- Future scalability with a relational database, ensuring ACID compliance.

### 3. Security of APIs
- **Authentication**: Token-based authentication using Django's default authentication system.
- **Role-based Access**: APIs like register and login are public, while others require authentication.
- **Data Protection**: Avoid exposing sensitive data unnecessarily (e.g., emails visible only to authorized users).
- **Input Validation**: Ensures payload correctness and prevents malicious injections.

### 4. Data Modeling
- **User Model**:  
  Includes fields like `phone_number`, `email`, `status` (enabled/disabled).  
  Designed to support both registered and unregistered numbers.
- **Spam Reports**:  
  Tracks spam with categories (unclassified, telemarketing, etc.) and optional comments.
- **Contacts**:  
  Maintains who added the contact and resolves conflicting names.

### 5. Structure of Code
- Modularized apps (`users`, `core`) for clean separation of concerns.
- Reusable serializers for shared validation and data transformations.
- Centralized settings for easy configuration.

### 6. Readability of Code
- Follows PEP 8 standards for clean and maintainable code.
- Docstrings and comments are added for clarity.
- Consistent naming conventions for variables and methods.

Here's the markdown content for your instructions:


# Project Setup Instructions

## Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Apply Database Migrations
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

## Create a Superuser
```bash
python manage.py createsuperuser
```

## Run the Development Server
```bash
python manage.py runserver
```

## API Documentation
Swagger UI is configured for interactive API documentation.
Visit http://127.0.0.1:8000/swagger/ after starting the server. (Set DEBUG=False)

## Testing
Run tests to ensure correctness:
```bash
\spamshield> pytest
```

## Logging
Configured logging to capture:
- API requests and responses.
- Authentication errors and validation failures.

Logs are written to both the console and a `logs/app.log` file for audit purposes.
