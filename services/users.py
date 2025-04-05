from flask import request, jsonify
from flask_restful import Resource
from models.models import db, User

class CreateUser(Resource):
    def post(self):
        data = request.json
        user = User(full_name=data['full_name'], email=data['email'], phone_number=data['phone_number'], password_hash=data['password'])
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully", "user_id": user.user_id}, 201


class GetUser(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return jsonify({"user_id": user.user_id, "full_name": user.full_name, "email": user.email, "phone": user.phone_number})

class GetUserIdByPhone(Resource):
    def post(self):
        data = request.json
        phone = data["phone"] 
        user = User.query.filter_by(phone_number=phone).first()
        if not user:
            return {"message": "User not Found."}, 404
        return jsonify({"user_id": user.user_id, "full_name": user.full_name, "email": user.email, "phone": user.phone_number})