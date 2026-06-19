# Gym Subscription Management API

A backend REST API for managing gym memberships, subscriptions, and payments. Built with FastAPI and PostgreSQL, with automated email reminders and scheduled subscription expiry.

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **PostgreSQL** — database
- **Alembic** — database migrations
- **JWT** — authentication
- **APScheduler** — background job scheduling
- **smtplib** — email notifications
- **Pydantic** — request/response validation
- **Passlib + bcrypt** — password hashing

## Features

- JWT-based authentication (register, login)
- Full CRUD for gym members
- Subscription management with renewal and auto-expiry
- Payment tracking with revenue aggregation
- Dashboard with live stats (total members, active/expired subscriptions, total revenue)
- Automated daily email reminders for subscriptions expiring the next day
- Scheduled nightly job to auto-mark expired subscriptions
- Multi-tenant: each gym owner only sees their own data

## Project Structure

```
gym-management-api/
├── main.py
├── scheduler.py
├── requirements.txt
├── .env
├── .env.example
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
├── core/
│   ├── auth.py
│   ├── config.py
│   └── security.py
├── database/
│   ├── db.py
│   ├── models.py
│   └── schemas.py
├── routers/
│   ├── auth.py
│   ├── members.py
│   ├── subscriptions.py
│   ├── payments.py
│   └── dashboard.py
└── services/
    ├── member_service.py
    ├── subscription_service.py
    ├── payment_service.py
    ├── dashboard_service.py
    ├── email_service.py
    └── reminder_service.py
```

## Setup

**1. Clone the repository**

```bash
git clone https://github.com/your-username/gym-management-api.git
cd gym-management-api
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```
DATABASE_URL=postgresql://user:password@localhost:5432/gym_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=30
EMAIL_ADDRESS=youremail@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
```

For `EMAIL_PASSWORD`, use a Gmail App Password, not your actual Gmail password. Generate one at Google Account > Security > App Passwords.

**5. Run database migrations**

```bash
alembic upgrade head
```

**6. Start the server**

```bash
uvicorn main:app --reload
```

API will be live at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new gym owner account |
| POST | `/auth/login` | Login and receive a JWT token |

### Members

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/members` | Add a new gym member |
| GET | `/members` | Get all members |
| GET | `/members/{member_id}` | Get a specific member |
| GET | `/members/search?name=` | Search members by name |
| PUT | `/members/{member_id}` | Update member details |
| DELETE | `/members/{member_id}` | Delete a member |

### Subscriptions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/subscriptions` | Create a subscription for a member |
| GET | `/subscriptions` | Get all subscriptions |
| GET | `/subscriptions/{subscription_id}` | Get a specific subscription |
| POST | `/subscriptions/{subscription_id}/renew` | Renew a subscription by 30 days |
| DELETE | `/subscriptions/{subscription_id}` | Cancel a subscription |

### Payments

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/payments` | Record a payment |
| GET | `/payments` | Get all payments |
| GET | `/payments/{payment_id}` | Get a specific payment |
| GET | `/payments/member/{member_id}` | Get all payments for a member |
| GET | `/payments/revenue` | Get total revenue |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard` | Get stats: total members, active/expired subscriptions, total revenue |

All endpoints except `/auth/register` and `/auth/login` require a Bearer token in the Authorization header.

## Authentication

After logging in, include the token in every request:

```
Authorization: Bearer <your_token>
```

## Scheduled Jobs

Two background jobs run automatically on server startup:

**Subscription expiry** — runs every day at midnight. Marks any subscription whose `end_date` has passed as `expired`.

**Email reminders** — runs every day at 9 AM. Sends an email to every member whose subscription expires the next day.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Secret key for JWT signing |
| `ALGORITHM` | JWT algorithm (use `HS256`) |
| `TOKEN_EXPIRE_MINUTES` | JWT expiry duration in minutes |
| `EMAIL_ADDRESS` | Gmail address used to send reminders |
| `EMAIL_PASSWORD` | Gmail App Password |

## Running Tests

```bash
pytest tests/ -v
```

Tests use an in-memory SQLite database and cover all routers: auth, members, subscriptions, payments, and dashboard. Each test function runs in an isolated database so tests never affect each other.