from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from backend.database.models import User, BankAccount
from backend import db
import random
import string

bp = Blueprint('auth', __name__)

def generate_account_number():
    """Generate a random 12-digit account number"""
    return ''.join(random.choices(string.digits, k=12))

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        
        # Validate required fields
        if not all([username, email, password, confirm_password, first_name, last_name, phone]):
            flash('All fields are required')
            return redirect(url_for('auth.signup'))
        
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('auth.signup'))
            
        if len(password) < 8:
            flash('Password must be at least 8 characters long')
            return redirect(url_for('auth.signup'))
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.signup'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        user.set_password(password)
        
        # Create bank account for user
        account = BankAccount(
            account_number=generate_account_number(),
            account_type='Savings',
            balance=0.0
        )
        
        user.account = account
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please login with your credentials.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.')
            return redirect(url_for('auth.signup'))
    
    return render_template('signup.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        if not username or not password:
            flash('Please enter both username and password')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            session['user_name'] = f"{user.first_name} {user.last_name}"
            flash(f'Welcome back, {user.first_name}!')
            return redirect(next_page if next_page else url_for('views.dashboard'))
        
        flash('Invalid username or password')
        return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    name = session.get('user_name', 'User')
    logout_user()
    session.clear()
    flash(f'Logged out successfully. Goodbye, {name}!')
    return redirect(url_for('views.index'))  # Redirect to landing page instead of login
