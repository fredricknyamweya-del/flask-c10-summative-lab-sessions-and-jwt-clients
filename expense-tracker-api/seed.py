"""
Seed script to populate database with test data.
"""
from faker import Faker
from datetime import datetime, timedelta
import random

from app import app, db
from models import User, Expense

fake = Faker()

def seed_database():
    """Populate database with test data."""
    
    with app.app_context():
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        print("Creating test users...")
        test_users = []
        usernames = ['alice', 'bob', 'charlie', 'diana', 'eve']
        
        for username in usernames:
            user = User(
                username=username,
                email=f'{username}@example.com'
            )
            user.set_password('password123')
            test_users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print(f"✓ Created {len(test_users)} test users")
        
        print("Creating sample expenses...")
        categories = ['Food', 'Transportation', 'Entertainment', 'Utilities', 'Shopping', 'Health', 'Education', 'Other']
        total_expenses = 0
        
        for user in test_users:
            num_expenses = random.randint(8, 15)
            
            for _ in range(num_expenses):
                days_ago = random.randint(0, 90)
                expense_date = datetime.utcnow() - timedelta(days=days_ago)
                
                expense = Expense(
                    user_id=user.id,
                    title=fake.sentence(nb_words=3).rstrip('.'),
                    description=fake.sentence(nb_words=8) if random.random() > 0.3 else None,
                    amount=round(random.uniform(5.0, 200.0), 2),
                    category=random.choice(categories),
                    date=expense_date
                )
                db.session.add(expense)
                total_expenses += 1
        
        db.session.commit()
        print(f"✓ Created {total_expenses} sample expenses")
        
        print("\n" + "="*50)
        print("DATABASE SEEDED SUCCESSFULLY")
        print("="*50)
        print(f"Test Users: {len(test_users)}")
        for user in test_users:
            expense_count = Expense.query.filter_by(user_id=user.id).count()
            print(f"  - {user.username} ({user.email}): {expense_count} expenses")
        print(f"\nTotal Expenses: {total_expenses}")
        print("\nTest Credentials:")
        for user in test_users:
            print(f"  - Username: {user.username}, Password: password123")
        print("="*50)


if __name__ == '__main__':
    seed_database()