# Expense Tracker Full Stack (Flask + React JWT Client)

This project includes:

- A Flask backend API for authentication and expense management
- A React frontend (`client-with-jwt`) that handles JWT login/signup/session persistence

Use this README as the single source of truth for setting up and running both services.

## Project Structure

```text
expense-tracker-api/
	app.py
	config.py
	models.py
	seed.py
	Pipfile
	client-with-jwt/
	client-with-sessions/
```

## Features

- JWT authentication (`/signup`, `/login`, `/me`)
- Password hashing with bcrypt
- Expense CRUD endpoints (user-scoped)
- Pagination support for list endpoints
- React client with persisted auth session via localStorage token

## Tech Stack

### Backend

- Flask
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Bcrypt
- Flask-Migrate
- SQLite

### Frontend

- React
- Fetch API

## Prerequisites

- Python 3.x
- Pipenv
- Node.js 18+ and npm

## Backend Setup

From the `expense-tracker-api` directory:

```bash
pipenv install
python -c "from app import app, db; app.app_context().push(); db.create_all()"
pipenv run python seed.py
```

## Run Backend

```bash
cd expense-tracker-api
pipenv run python app.py
```

Backend runs on:

`http://localhost:5000`

## Frontend Setup (JWT Client)

In a second terminal:

```bash
cd expense-tracker-api/client-with-jwt
npm install
npm start
```

Frontend runs on:

`http://localhost:3000`

## End-to-End Run Order

1. Start backend (`http://localhost:5000`)
2. Start frontend (`http://localhost:3000`)
3. Sign up or log in from the frontend
4. Frontend stores token and calls protected endpoints using `Authorization: Bearer <token>`

## Required Auth Endpoints

The JWT client expects these routes to exist:

### POST /signup

Request:

```json
{
	"username": "string",
	"password": "string",
	"password_confirmation": "string"
}
```

Response:

```json
{
	"token": "<JWT string>",
	"user": {
		"id": 1,
		"username": "string"
	}
}
```

### POST /login

Request:

```json
{
	"username": "string",
	"password": "string"
}
```

Response:

```json
{
	"token": "<JWT string>",
	"user": {
		"id": 1,
		"username": "string"
	}
}
```

### GET /me

Headers:

```http
Authorization: Bearer <token>
```

Response:

```json
{
	"id": 1,
	"username": "string"
}
```

## Protected Resource Expectations

For expense routes (or any custom resource), ensure:

- JWT required on all resource endpoints
- Data is scoped to the authenticated user
- REST methods are implemented (`GET`, `POST`, `PATCH`, `DELETE`)
- List endpoint supports pagination (`?page=1&per_page=10`)

## Troubleshooting

- `401 Unauthorized`:
	- Confirm token is sent as `Bearer <token>`
	- Confirm token is valid and not expired
- CORS errors:
	- Ensure backend allows requests from `http://localhost:3000`
- Frontend cannot reach backend:
	- Confirm backend is running on port `5000`
	- Confirm frontend request URLs/proxy config

## Development Notes

- `client-with-jwt` is the JWT-focused frontend for this backend.
- `client-with-sessions` is included for session-auth workflows and is not required for JWT flow.