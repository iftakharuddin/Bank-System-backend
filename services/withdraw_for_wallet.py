import jwt
import random
from flask import request
from flask_restful import Resource
from models.models import *
from forms.forms import *
from services.response_handler import *
from decimal import Decimal

SECRET_KEY = "your_secret_key"  # Change this securely

class VerifyTransaction(Resource):
    def post(self):
        form = VerifyTransactionForm()

        if not form.validate_on_submit():
            return ResponseHandler.generate("E002", data=form.errors)

        data = request.json
        token = data.get("token")
        amount = Decimal(data.get("amount"))

        # Decode token
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            wallet_id = decoded["wallet_id"]
            bank_account_number = decoded["bank_account_number"]
        except jwt.ExpiredSignatureError:
            return {"message": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Invalid token"}, 401

        # Check if the bank account is active
        bank_account = BankAccount.query.get(bank_account_number)
        if not bank_account or not bank_account.is_active:
            return {"message": "Invalid token or inactive account"}, 403

        # Check if sufficient balance for withdrawal
        if amount > bank_account.balance:
            return ResponseHandler.generate("E005")

        # Generate OTP and store transaction
        otp = str(random.randint(100000, 999999))
        transaction = Transaction(
            from_account=bank_account_number,
            amount=amount,
            otp=otp,
            to_wallet_id=wallet_id
        )
        db.session.add(transaction)
        db.session.commit()

        user = User.query.filter_by(user_id=bank_account.user_id).first()
        # Simulate sending OTP
        print(f"OTP for {user.phone_number}: {otp}")

        return ResponseHandler.generate("S001", data={
            "message": "OTP sent to registered mobile number",
            "transaction_id": transaction.transaction_id
        })


class VerifyOTPWithdraw(Resource):
    def post(self):
        form = OTPTransactionForm()
        if not form.validate_on_submit():
            return ResponseHandler.generate("E002", data=form.errors)

        data = request.json
        transaction_id = data.get("transaction_id")
        otp = data.get("otp")

        # Find transaction
        transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()

        if not transaction or transaction.otp != otp:
            return ResponseHandler.generate("E006")

        # Deduct amount from bank account
        bank_account = BankAccount.query.get(transaction.from_account)
        if bank_account.balance < transaction.amount:
            return ResponseHandler.generate("E005")

        bank_account.balance -= transaction.amount
        transaction.status = "completed"

        db.session.commit()

        return ResponseHandler.generate("S001", data={
            "message": "Transaction successful",
        })
