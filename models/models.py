from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum
import uuid

db = SQLAlchemy()

class AccountType(Enum):
    SAVINGS = "savings"
    CHECKING = "checking"

class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

# Users Table
class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bank_accounts = db.relationship('BankAccount', backref='user', cascade="all, delete", lazy=True)

# Bank Accounts Table
class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'
    
    account_number = db.Column(db.String(20), primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    account_type = db.Column(db.Enum(AccountType), nullable=False)
    balance = db.Column(db.Numeric(15,2), default=0.00, nullable=False)
    currency = db.Column(db.String(3), default="BDT", nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "account_number": self.account_number,
            "user_id": self.user_id,
            "account_type": self.account_type.value if self.account_type else None,  # Convert Enum to string
            "balance": float(self.balance),  # Convert Decimal to float for JSON compatibility
            "currency": self.currency,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None  # Format datetime to string
        }


class Transaction(db.Model):
    transaction_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    from_account = db.Column(db.String(20), db.ForeignKey("bank_accounts.account_number"), nullable=False)
    to_wallet_id = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(15,2), nullable=False)
    status = db.Column(db.Enum(TransactionStatus), default=TransactionStatus.PENDING)
    reference = db.Column(db.String(255), nullable=True)
    callback_url = db.Column(db.String(255), nullable=True)  # Webhook URL for System A
    otp = db.Column(db.String(6), nullable=True)


class WalletBankLink(db.Model):
    link_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    wallet_id = db.Column(db.String(50), nullable=False)
    bank_account_number = db.Column(db.String(20), db.ForeignKey('bank_accounts.account_number'), nullable=False)
    otp = db.Column(db.String(6), nullable=True)  # OTP for verification
    verified = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(1024), nullable=True)  # Token for future transactions



from werkzeug.security import generate_password_hash, check_password_hash


class APIClient(db.Model):
    client_id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    client_secret_hash = db.Column(db.String(255), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def set_secret(self, secret):
        self.client_secret_hash = generate_password_hash(secret)

    def check_secret(self, secret):
        return check_password_hash(self.client_secret_hash, secret)
