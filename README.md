# Contact Book Application

# Overview

This is a simple Contact Book API built using FastAPI.
It allows users to create, search, delete, and merge contacts.

# Steps to setup in your local machine

1. Clone the repository
    git clone https://github.com/BenJohnK/contact_book.git
    cd contact_book

2. Create virtual environment
    python3 -m venv venv source venv/bin/activate

3. Install dependencies
    pip install fastapi uvicorn

4. Run the application
    uvicorn main:app --reload

5. Access API
    Base URL: http://127.0.0.1:8000
    Swagger UI: http://127.0.0.1:8000/docs

# Design Decisions

1. Used FastAPI for rapid API development and built-in validation via Pydantic
2. Used in-memory storage (Python list) for simplicity and fast execution
3. UUID used for unique identification of contacts
4. Search implemented as case-insensitive partial match across multiple fields

# Contacts Merge Logic

1. Non-empty values are preferred
2. A new contact is created with merged data
3. Original contacts are removed

# Production Architecture (If deployed as a web app)

## Backend
1. FastAPI (Python) for REST APIs
2. Service layer to handle business logic

## Frontend
1. React / Next.js for UI

## Database
1. PostgreSQL for persistent storage
2. Proper indexing on name, email, phone for fast search

## Caching
1. Redis for caching frequent search queries
2. Search Optimization

## Background Jobs
1. Celery + Redis for async tasks (e.g., deduplication, bulk imports)

## Deployment
1. Backend: Docker + AWS EC2 / ECS
2. Database: AWS RDS
3. Frontend: Vercel / S3 + CloudFront

## Security
1. JWT-based authentication
2. Input validation and sanitization
3. Rate limiting