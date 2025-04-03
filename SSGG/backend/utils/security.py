from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def validate_transaction(amount, account):
    """Validate if a transaction can be performed"""
    if amount <= 0:
        return False, "Amount must be positive"
    
    if amount > account.balance and transaction_type == 'debit':
        return False, "Insufficient funds"
    
    return True, "Transaction valid"

def mask_account_number(account_number):
    """Mask middle digits of account number"""
    if len(account_number) < 8:
        return account_number
    return f"{account_number[:4]}****{account_number[-4:]}"
