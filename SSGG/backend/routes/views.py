from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from flask_login import login_required, current_user
from backend.database.models import User, BankAccount
from backend import db
from datetime import datetime
import pytz

bp = Blueprint('views', __name__)

@bp.context_processor
def inject_current_year():
    return {
        'current_year': datetime.now().year,
        'current_time': datetime.now(pytz.timezone('Asia/Kolkata'))
    }

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        # Get user and account details
        user = User.query.get(current_user.id)
        account = BankAccount.query.filter_by(user_id=current_user.id).first()
        return render_template('dashboard.html', user=user, account=account)
    return redirect(url_for('views.index'))

@bp.route('/profile')
@login_required
def profile():
    # Get user and account details
    user = User.query.get(current_user.id)
    account = BankAccount.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', user=user, account=account)

@bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    user = User.query.get(current_user.id)
    
    # Get form data
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    
    # Validate required fields
    if not all([first_name, last_name, email, phone]):
        flash('All fields are required')
        return redirect(url_for('views.profile'))
    
    # Check if email is already taken by another user
    existing_user = User.query.filter_by(email=email).first()
    if existing_user and existing_user.id != current_user.id:
        flash('Email already registered with another account')
        return redirect(url_for('views.profile'))
    
    # Update user details
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.phone = phone
    
    try:
        db.session.commit()
        session['user_name'] = f"{user.first_name} {user.last_name}"  # Update session name
        flash('Profile updated successfully')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating your profile')
    
    return redirect(url_for('views.profile'))

@bp.route('/investments')
@login_required
def investments():
    return render_template('investments.html')

@bp.route('/bills')
@login_required
def bills():
    return render_template('bills.html')

@bp.route('/security')
@login_required
def security():
    user = User.query.get(current_user.id)
    return render_template('security.html', user=user)

@bp.route('/loans')
@login_required
def loans():
    return render_template('loans.html')

@bp.route('/transfer')
@login_required
def transfer():
    return render_template('transfer.html')

@bp.route('/blockchain')
@login_required
def blockchain():
    blockchain_data = {
        'latest_block': {
            'hash': '0x7d8f...',
            'timestamp': datetime.now(pytz.timezone('Asia/Kolkata')),
            'transactions': 156,
            'smart_contracts': 3
        },
        'smart_contracts': [
            {
                'name': 'SecureTransaction',
                'address': '0x1234...',
                'type': 'Payment Gateway',
                'status': 'Active',
                'transactions': 89
            },
            {
                'name': 'LoanContract',
                'address': '0x5678...',
                'type': 'Loan Management',
                'status': 'Active',
                'transactions': 45
            },
            {
                'name': 'InvestmentPool',
                'address': '0x9abc...',
                'type': 'Investment',
                'status': 'Active',
                'transactions': 22
            }
        ],
        'recent_transactions': [
            {
                'hash': '0xabcd...',
                'type': 'Fund Transfer',
                'status': 'Confirmed',
                'time': '2 minutes ago'
            },
            {
                'hash': '0xdef0...',
                'type': 'Smart Contract Call',
                'status': 'Confirmed',
                'time': '5 minutes ago'
            },
            {
                'hash': '0x1234...',
                'type': 'Loan Approval',
                'status': 'Pending',
                'time': '7 minutes ago'
            }
        ]
    }
    return render_template('blockchain.html', data=blockchain_data)

@bp.route('/faq')
def faq():
    return render_template('faq.html')
