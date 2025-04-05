from flask import request, jsonify
from flask_restful import Resource
from models.models import db, BankAccount, User

class CreateAccount(Resource):
    def post(self):
        data = request.json
        new_account = BankAccount(
            account_number=data['account_number'],
            user_id=data['user_id'],
            account_type=data['account_type'],
            balance=data['balance']
        )
        db.session.add(new_account)
        db.session.commit()
        return {"message": "Bank account created"}, 201

    
class GetAllUserAccounts(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        all = []
        for each in user.bank_accounts: 
            all.append(each.to_dict())
        return {"user_id": user.user_id, "Owner": user.full_name ,"accounts": all}
        

class GetBalance(Resource):
    def get(self, account_number):
        account = BankAccount.query.get(account_number)
        if not account:
            return {"message": "Account not found"}, 404
        return {"balance": float(account.balance)}
