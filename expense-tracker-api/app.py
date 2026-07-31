"""
Expense Tracker Flask API with JWT Authentication.
Full CRUD operations for user-owned expenses.
"""
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from datetime import datetime
import os

from config import config
from models import db, bcrypt, User, Expense

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config[os.environ.get('FLASK_ENV', 'development')])

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


# AUTH ENDPOINTS

@app.route('/auth/signup', methods=['POST'])
def signup():
    """Register a new user."""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409
        
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/auth/login', methods=['POST'])
def login():
    """Login user and return JWT access token."""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing username or password'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user's profile."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# EXPENSE ENDPOINTS

@app.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    """Get all expenses for authenticated user with pagination."""
    try:
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        if page < 1 or per_page < 1:
            return jsonify({'error': 'Invalid pagination parameters'}), 400
        
        paginated = Expense.query.filter_by(user_id=user_id).order_by(
            Expense.date.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'expenses': [expense.to_dict() for expense in paginated.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/expenses', methods=['POST'])
@jwt_required()
def create_expense():
    """Create a new expense for authenticated user."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('title') or data.get('amount') is None:
            return jsonify({'error': 'Title and amount are required'}), 400
        
        try:
            amount = float(data['amount'])
            if amount < 0:
                return jsonify({'error': 'Amount must be positive'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid amount'}), 400
        
        expense_date = datetime.utcnow()
        if data.get('date'):
            try:
                expense_date = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
            except:
                return jsonify({'error': 'Invalid date format'}), 400
        
        expense = Expense(
            user_id=user_id,
            title=data['title'],
            description=data.get('description'),
            amount=amount,
            category=data.get('category', 'Other'),
            date=expense_date
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({
            'message': 'Expense created successfully',
            'expense': expense.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/expenses/<int:expense_id>', methods=['GET'])
@jwt_required()
def get_expense(expense_id):
    """Get a specific expense by ID."""
    try:
        user_id = get_jwt_identity()
        expense = Expense.query.get(expense_id)
        
        if not expense or expense.user_id != user_id:
            return jsonify({'error': 'Expense not found'}), 404
        
        return jsonify({'expense': expense.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/expenses/<int:expense_id>', methods=['PATCH'])
@jwt_required()
def update_expense(expense_id):
    """Update an expense."""
    try:
        user_id = get_jwt_identity()
        expense = Expense.query.get(expense_id)
        
        if not expense or expense.user_id != user_id:
            return jsonify({'error': 'Expense not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'title' in data:
            expense.title = data['title']
        if 'description' in data:
            expense.description = data['description']
        if 'amount' in data:
            try:
                amount = float(data['amount'])
                if amount < 0:
                    return jsonify({'error': 'Amount must be positive'}), 400
                expense.amount = amount
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid amount'}), 400
        if 'category' in data:
            expense.category = data['category']
        if 'date' in data:
            try:
                expense.date = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
            except:
                return jsonify({'error': 'Invalid date format'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Expense updated successfully',
            'expense': expense.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    """Delete an expense."""
    try:
        user_id = get_jwt_identity()
        expense = Expense.query.get(expense_id)
        
        if not expense or expense.user_id != user_id:
            return jsonify({'error': 'Expense not found'}), 404
        
        db.session.delete(expense)
        db.session.commit()
        
        return jsonify({'message': 'Expense deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



# ERROR HANDLERS

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'API is running'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)