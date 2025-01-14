# app/api/auth.py
from flask_restx import Namespace, Resource, fields
from flask import request
from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_ns = Namespace('auth', description="User Authentication")

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
})

signup_model = auth_ns.model('SignUp', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
})

@auth_ns.route('/register')
class RegisterResource(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        """Register a new user."""
        data = request.json
        if User.query.filter_by(username=data['username']).first():
            return {"message": "Username already taken."}, 400
        hashed_password = generate_password_hash(data['password'])
        user = User(username=data['username'], password=hashed_password, role="user")
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """User login to get a JWT token."""
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {"message": "Invalid credentials."}, 401

        if check_password_hash(user.password, data['password']):
            #access_token = create_access_token(identity={"username": user.username, "role": user.role})
            access_token = create_access_token(identity=user.username, additional_claims={"role": user.role})
            return {"access_token": access_token}, 200

        return {"message": "Invalid credentials."}, 401


@auth_ns.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """Protected route to verify JWT."""
        current_user = get_jwt_identity()  # {'username':..., 'role':...}
        return {"logged_in_as": current_user}, 200
