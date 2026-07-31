# Expense Tracker API

A secure, JWT-authenticated Flask REST API for tracking personal expenses. Users can register, login, and manage their own expenses with full CRUD operations.

## Features

- **User Authentication**: Secure signup, login, and profile endpoints using JWT
- **Password Security**: Passwords hashed with bcrypt before storage
- **Expense Management**: Full CRUD operations for user expenses
- **Pagination**: Paginated expense listing with customizable page size
- **User Isolation**: Users can only access their own expenses
- **RESTful API**: Clean, RESTful endpoint design with proper HTTP status codes
- **Error Handling**: Comprehensive error messages and validation

## Tech Stack

- **Framework**: Flask 2.2.2
- **Database**: SQLAlchemy with SQLite (production-ready for PostgreSQL)
- **Authentication**: JWT (Flask-JWT-Extended)
- **Password Hashing**: bcrypt
- **Migrations**: Flask-Migrate
- **Validation**: Marshmallow

## Project Structure

```
expense-tracker-api/
├── app.py              # Main Flask application with all routes
├── models.py           # Database models (User, Expense)
├── config.py           # Configuration settings
├── seed.py             # Database seeding script
├── Pipfile             # Python dependencies
├── .gitignore          # Git ignore rules
├── migrations/         # Database migration files (generated)
└── README.md           # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip or pipenv

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd expense-tracker-api
```

### Step 2: Install Dependencies

Using pipenv (recommended):

```bash
pipenv install
pipenv shell
```

Or using pip:

```bash
pip install -r requirements.txt
# If no requirements.txt, install from Pipfile manually
pip install flask==2.2.2 flask-sqlalchemy==3.0.3 flask-jwt-extended==4.4.4 flask-bcrypt==1.0.1 flask-migrate==4.0.0 faker==15.3.2
```

### Step 3: Initialize Database

```bash
# Create database and run migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Step 4: Seed Database (Optional)

```bash
# Populate database with test data
python seed.py
```

This creates 5 test users (alice, bob, charlie, diana, eve) with sample expenses.

## Running the Application

### Development Server

```bash
# Using Flask
flask run

# Or using Python directly
python app.py
```

The API will be available at `http://localhost:5000`

### Health Check

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{"status": "API is running"}
```

## API Endpoints

### Authentication Endpoints

#### POST `/auth/signup`
Register a new user.

**Request Body:**
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

#### POST `/auth/login`
Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "username": "alice",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

#### GET `/auth/me`
Get current authenticated user's profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

### Expense Endpoints

#### GET `/expenses`
Get all expenses for authenticated user (paginated).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (int, default: 1) - Page number
- `per_page` (int, default: 10, max: 100) - Items per page

**Response (200 OK):**
```json
{
  "expenses": [
    {
      "id": 1,
      "user_id": 1,
      "title": "Lunch at cafe",
      "description": "Lunch with colleagues",
      "amount": 15.50,
      "category": "Food",
      "date": "2024-01-15T12:30:00",
      "created_at": "2024-01-15T12:35:00",
      "updated_at": "2024-01-15T12:35:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "pages": 3
  }
}
```

---

#### POST `/expenses`
Create a new expense.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "title": "Grocery shopping",
  "description": "Weekly groceries",
  "amount": 65.99,
  "category": "Shopping",
  "date": "2024-01-15T14:00:00"
}
```

**Response (201 Created):**
```json
{
  "message": "Expense created successfully",
  "expense": {
    "id": 2,
    "user_id": 1,
    "title": "Grocery shopping",
    "description": "Weekly groceries",
    "amount": 65.99,
    "category": "Shopping",
    "date": "2024-01-15T14:00:00",
    "created_at": "2024-01-15T14:05:00",
    "updated_at": "2024-01-15T14:05:00"
  }
}
```

---

#### GET `/expenses/<id>`
Get a specific expense by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "expense": {
    "id": 1,
    "user_id": 1,
    "title": "Lunch at cafe",
    "description": "Lunch with colleagues",
    "amount": 15.50,
    "category": "Food",
    "date": "2024-01-15T12:30:00",
    "created_at": "2024-01-15T12:35:00",
    "updated_at": "2024-01-15T12:35:00"
  }
}
```

---

#### PATCH `/expenses/<id>`
Update an existing expense.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body (any fields to update):**
```json
{
  "amount": 18.75,
  "category": "Food"
}
```

**Response (200 OK):**
```json
{
  "message": "Expense updated successfully",
  "expense": {
    "id": 1,
    "user_id": 1,
    "title": "Lunch at cafe",
    "description": "Lunch with colleagues",
    "amount": 18.75,
    "category": "Food",
    "date": "2024-01-15T12:30:00",
    "created_at": "2024-01-15T12:35:00",
    "updated_at": "2024-01-15T14:10:00"
  }
}
```

---

#### DELETE `/expenses/<id>`
Delete an expense.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Expense deleted successfully"
}
```

---

## Error Responses

### 400 Bad Request
```json
{"error": "Missing required fields"}
```

### 401 Unauthorized
```json
{"error": "Invalid username or password"}
```

### 404 Not Found
```json
{"error": "Expense not found"}
```

### 409 Conflict
```json
{"error": "Username already exists"}
```

### 500 Internal Server Error
```json
{"error": "Internal server error"}
```

## Testing the API

### Using Postman

1. **Signup**: POST to `http://localhost:5000/auth/signup`
   - Body (raw JSON): username, email, password

2. **Login**: POST to `http://localhost:5000/auth/login`
   - Body (raw JSON): username, password
   - Copy the `access_token` from response

3. **Add Token to Headers**:
   - All subsequent requests need `Authorization: Bearer <access_token>` header

4. **Test Expense Endpoints**: Create, read, update, delete expenses

### Using curl

```bash
# Signup
curl -X POST http://localhost:5000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"pass123"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"pass123"}'

# Get expenses (replace TOKEN with actual token)
curl -X GET http://localhost:5000/expenses \
  -H "Authorization: Bearer TOKEN"

# Create expense
curl -X POST http://localhost:5000/expenses \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Lunch","amount":15.50,"category":"Food"}'
```

## Security Features

- ✅ Passwords hashed with bcrypt
- ✅ JWT tokens for stateless authentication
- ✅ User isolation (users only access their own data)
- ✅ Input validation on all endpoints
- ✅ Error messages don't leak sensitive information
- ✅ 24-hour token expiration

## Database Models

### User
- `id`: Primary key
- `username`: Unique, indexed
- `email`: Unique, indexed
- `password_hash`: Bcrypt hashed password
- `created_at`: Timestamp

### Expense
- `id`: Primary key
- `user_id`: Foreign key to User
- `title`: Expense description
- `description`: Optional longer description
- `amount`: Expense amount (float)
- `category`: Expense category
- `date`: Date of expense
- `created_at`: Created timestamp
- `updated_at`: Last updated timestamp

## Environment Variables

Create a `.env` file (optional):

```env
FLASK_ENV=development
FLASK_APP=app.py
DATABASE_URL=sqlite:///expense_tracker.db
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

## Deployment

For production:

1. Set `FLASK_ENV=production`
2. Change `SECRET_KEY` and `JWT_SECRET_KEY` to secure values
3. Use PostgreSQL instead of SQLite
4. Deploy with Gunicorn: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
5. Use environment variables for configuration

## Troubleshooting

### ModuleNotFoundError
Make sure you're in the virtual environment: `pipenv shell`

### Database locked
Delete `expense_tracker.db` and re-run `flask db upgrade`

### JWT token expired
Login again to get a new token

### Port already in use
Change port: `flask run --port 5001`

## Future Enhancements

- [ ] Add expense filtering by date range
- [ ] Add expense statistics/analytics
- [ ] Add budget limits and alerts
- [ ] Add expense categories management
- [ ] Add recurring expenses
- [ ] Add expense export to CSV
- [ ] Add multi-currency support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Author

Fredrick Nyamweya - Moringa School Student (SDF-FTR17M3)

## Support

For issues or questions, open an issue on GitHub or contact the instructor.