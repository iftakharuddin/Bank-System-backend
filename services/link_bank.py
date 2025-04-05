from flask import request, jsonify
from flask_restful import Resource
import random
from models.models import *
import jwt
import datetime
from services.response_handler import *
from forms.forms import *

class VerifyBankAccount(Resource):
    def post(self):
        form = VerifyAccountForm()
        if not form.validate_on_submit():
            return ResponseHandler.generate("E002", data=form.errors)

        data = request.json
        bank_account = BankAccount.query.get(data["bank_account_number"])

        if not bank_account:
            return ResponseHandler.generate("E001")

        owner = data.get("owner")
        user = User.query.filter_by(user_id=bank_account.user_id).first()

        if owner != user.full_name:
            return ResponseHandler.generate("E003")

        wallet_id = data.get("wallet_id")
        bank_account_no = data.get("bank_account_number")

        prev_link = WalletBankLink.query.filter_by(wallet_id=wallet_id, bank_account_number=bank_account_no).first()
        if prev_link:
            db.session.delete(prev_link)
            db.session.commit()
        # Generate OTP and store in the database
        otp = str(random.randint(100000, 999999))
        link_entry = WalletBankLink(
            wallet_id=data["wallet_id"],
            bank_account_number=data["bank_account_number"],
            otp=otp
        )
        db.session.add(link_entry)
        db.session.commit()

        # Simulate sending OTP to user's phone
        print(f"OTP for {user.phone_number}: {otp}")

        return ResponseHandler.generate("S001", data={"link_id": link_entry.link_id})



SECRET_KEY = "your_secret_key"  # Change this to a secure key

class VerifyOTPForLinkBank(Resource):
    def post(self):
        form = OTPforLinkForm()

        if not form.validate_on_submit():
            return ResponseHandler.generate("E002", data=form.errors)
        
        data = request.json
        link_entry = WalletBankLink.query.get(data["link_id"])

        if not link_entry or link_entry.otp != data["otp"]:
            return ResponseHandler.generate("E004")

        # Generate JWT Token for the linked bank account
        token_payload = {
            "wallet_id": link_entry.wallet_id,
            "bank_account_number": link_entry.bank_account_number,
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

        # Store the token in the database
        link_entry.verified = True
        link_entry.token = token
        db.session.commit()

        return ResponseHandler.generate("S001", data={"message": "Bank account successfully linked", "token": token})
