# Restaurant Review API

This is a Flask-based **Restaurant Review API**.  
It manages restaurants and reviews with JWT auth, caching, 
request rate limiting, provides basic analytics and optional async endpoint.

## Features
1.  **Restaurant Management**: Create, retrieve restaurants.
2. **Review Management**: Submit, retrieve, approve reviews.
3.  **Analytics**:
    - Average rating per restaurant
    - Top 3 restaurants by cuisine
4. **Security**:
   - JWT-based Auth (admin/user)
   - Role-based access
   - Request rate limiting

## Tech Stack

- **Python** 3.10+
- **Flask** 2.x (Flask-RESTX for docs)
- **SQLAlchemy** + **Marshmallow**
- **PostgreSQL** or **SQLite**
- **Flask-Limiter** (for rate limiting)
- **Pytest** (for testing)

## Project structure
- restaurant_api
   ```bash
   restaurant_api/
   ├── app/
   │   ├── __init__.py (creates and configures Flask instance)
   │   ├── config.py (all config classes)
   │   ├── models/ (SQLAlchemy models)
   │   ├── schemas/ (Marshmallow schemas)
   │   ├── api/ (RESTX namespaces/endpoints)
   │   ├── services/ (business logic, optional)
   │   └── utils/ (helper functions, limiters, custom exceptions)
   ├── tests/
   │   ├── conftest.py (fixtures, e.g., create_app)
   │   ├── test_*.py (test files)
   ├── requirements.txt
   ├── README.md
   └── .env


## Quick Start

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/krishnapawankar/restaurant_api.git
   cd restaurant_api
   
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Activate on Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Database Migrations (if using Flask-Migrate + Postgres):**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade

5. **Run the Application:**
   ```bash
   flask run
   The API will be at http://127.0.0.1:5000/api/

6. **Usage**
   ```bash
   Swagger UI: Go to http://127.0.0.1:5000/api/ to see interactive docs.
   Sample Endpoints:
   POST /auth/register → Register user
   POST /auth/login → Obtain JWT token
   POST /restaurants → Create restaurant (admin only)
   POST /reviews → Submit review (logged-in user)

7. **Testing**
   ```bash
   pytest --cov=app --cov-report=term-missing

8. **Assumptions**
   ```bash
   First registered user can be made admin via update query.
   We store roles in role field (admin vs user).
   Rate-limiting is set to 5/min on certain endpoints.
   No password reset functionality.
   Review status defaults to PENDING
