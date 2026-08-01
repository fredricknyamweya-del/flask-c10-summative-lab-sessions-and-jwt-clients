# Expense Tracker API

A secure, JWT-authenticated Flask REST API for tracking personal expenses.

## Features

- **User Authentication**: Secure signup, login, and profile endpoints using JWT
- **Password Security**: Passwords hashed with bcrypt before storage
- **Expense Management**: Full CRUD operations for user expenses
- **Pagination**: Paginated expense listing with customizable page size
- **User Isolation**: Users can only access their own expenses
- **RESTful API**: Clean endpoint design with proper HTTP status codes

## Tech Stack

- Flask 2.2.2
- SQLAlchemy with SQLite
- JWT (Flask-JWT-Extended)
- Bcrypt
- Flask-Migrate

## Installation

```bash
# Install dependencies
pipenv install

# Create database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Seed database
pipenv run python seed.py
```

## Running the API

```bash
pipenv shell
python app.py
```

API runs at: `http://localhost:5000`

## Test Credentials