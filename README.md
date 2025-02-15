# ProjectX - Household Tasks Manager

A FastAPI-based REST API application for managing household tasks and tracking user statistics.

## Project Description

ProjectX is a household task management system that allows users to create, manage, and track household tasks. The application includes user management, task tracking, and statistical analysis features.

## Components

The project consists of the following main components:

### Backend (API)

- **Controllers**: Handle HTTP requests and route them to appropriate services
  - User Controller: Manages user-related operations
  - Task Controller: Handles task management
  - Stats Controller: Provides statistical data
- **Services**: Contains business logic
- **Database**: SQLAlchemy-based models and connections
  - Models: User and Task entities
- **DTOs**: Data Transfer Objects for request/response handling

## Setup Instructions

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

- Windows:

```bash
.venv\Scripts\activate
```

- Unix/MacOS:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r .\api\requirements.txt
```

4. Run the application:

```bash
uvicorn app.main:app --reload --app-dir API
```

## API Documentation

Once the application is running, you can access:

- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`
