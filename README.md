# Subscription Management System with Currency Exchange Tracker
A Django-based system for managing user subscriptions with real-time currency exchange integration and background task processing using Celery.

## Features
1. Django REST Framework-based APIs for subscriptions
2. Celery task to log currency exchange rates periodically
3. External API integration (ExchangeRate-API)
4. Admin interface for managing subscriptions and plans
5. Basic frontend (non-SPA) using Bootstrap
6. JWT Authentication

## Requirements
1. Python
2. Django
3. Django REST Framework
4. Djangorestframework-simplejwt
5. Redis (for Celery)

## Local setup steps
### 1. Clone the repository
git clone https://github.com/sakhawat46/subscription-management-system.git

### 2. Create and activate a virtual environment
python -m venv venv <br>
venv\Scripts\activate (On Linax: source venv/bin/activate)

### 3. Navigate to the project directory
cd subscription-management-system

### 4. Install dependencies
pip install -r requirements.txt

### 5. Set environment variables
create .env file and write secret key info <br>
EXCHANGE_API_KEY="71d1c36a50bfaa7d66102767"

### 6. Run makemigrations
python manage.py makemigrations

### 7. Run migrations
python manage.py migrate

### 8. Create superuser
python manage.py createsuperuser

### 9. Run development server
python manage.py runserver


## How to run Celery
### 1. Firstly Redis install and run the redis server
Install for windows: https://github.com/tporadowski/redis/releases <br>
Run: Open Windows Powershell and write the command: redis-cli ping

### 2. Run Celery worker (in a separate terminal)
celery -A projects worker --loglevel=info --pool=solo

### 3. Run Celery beat scheduler (in another terminal)
celery -A projects beat --loglevel=info


## API endpoints (with examples)


### For access and refresh token
POST http://127.0.0.1:8000/api/token/
<br>
Request Body json:
{
  "username": "admin",
  "password": "admin"
}
<br>
Response:
<br>
<img width="844" height="184" alt="image" src="https://github.com/user-attachments/assets/12b20c01-5968-4f18-abe5-65b98a08fb44" />


### Subscribe to a Plan
POST http://127.0.0.1:8000/api/subscribe/
<br>
Need JWT authentication: Bearer <token>
<br>
Request Body json:
{
  "plan_id": 1
}
<br>
Response:
<br>
<img width="301" height="244" alt="image" src="https://github.com/user-attachments/assets/56edd723-1faa-44fa-b8f8-7a79eda19ca5" />


### User Subscriptions
GET http://127.0.0.1:8000/api/subscriptions/
<br>
Need JWT authentication: Bearer <token>
<br>
Response:
<br>
<img width="329" height="415" alt="image" src="https://github.com/user-attachments/assets/baf733d4-9b51-4925-87ae-35e0b670842e" />


### Cancel Subscription
POST http://127.0.0.1:8000/api/cancel/
<br>
Need JWT authentication: Bearer <token>
<br>
Request Body json:
{
  "subscription_id": 1
}
<br>
Response:
<br>
<img width="357" height="130" alt="image" src="https://github.com/user-attachments/assets/ddc09710-822a-4c84-a2d2-e48fbddfc8b3" />


### Currency Exchange Rate
GET http://127.0.0.1:8000/api/exchange-rate/?base=USD&target=BDT
<br>
Response:
<br>
<img width="331" height="223" alt="image" src="https://github.com/user-attachments/assets/94c920f8-5b2b-47c4-99d9-bb8ef2974ba1" />


## List all users and their subscriptions in a table
Users subscriptions list url: http://127.0.0.1:8000/subscriptions/ <br>
<img width="1188" height="357" alt="image" src="https://github.com/user-attachments/assets/1ffd7d0e-937d-47ca-929e-c3e8201d1420" />


## Project overview video
Link: https://app.usebubbles.com/ptoZUkgDX8GRAgYZU7YKAX