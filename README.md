# Dictionary API

A FastAPI-based REST API for managing dictionary items per user.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Add Dictionary Item
- **POST** `/dictionary`
- Request body:
```json
{
    "user_id": "string",
    "dictionary_item": "string"
}
```

### Get All Dictionary Items
- **GET** `/dictionary/{user_id}`

## Architecture

This project follows SOLID principles and clean architecture:
- Repository Pattern for data access
- Service Layer for business logic
- Dependency Injection
- Interface Segregation
- Single Responsibility Principle 