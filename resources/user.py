from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_refresh_token,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from sqlalchemy import or_
from db import db
from blocklist import BLOCKLIST
from models import UserModel, TokenBlocklist
from schemas import UserSchema, UserRegisterSchema
from utilities.mail_utils import send_email
from utilities.admin_decorator import admin_required
from task import enqueue_welcome_email

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register") 
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(UserModel.username == user_data["username"], UserModel.email == user_data["email"])
        ).first():
            abort(409, message="A user with that username or email already exists.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        
        if UserModel.query.count() == 0:
            user.is_admin = True
        else:
            user.is_admin = False
            
        db.session.add(user)
        db.session.commit()

        enqueue_welcome_email(
            user_data["email"],
            user_data["username"]
        )

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            
            additional_claims = {"is_admin": user.is_admin}
            
            access_token = create_access_token(identity=str(user.id), fresh=True, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=str(user.id))
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            },200
        
        abort(401, message="Invalid credentials")
        
        
    @blp.route("/refresh")
    class TokenRefresh(MethodView):
        @jwt_required(refresh=True)
        def post(self):
            current_user = get_jwt_identity()
            user = UserModel.query.get(current_user)
            additional_claims = {"is_admin": user.is_admin}
            new_token = create_access_token(identity=current_user, fresh=False, additional_claims=additional_claims)
            
            return {"access_token": new_token}, 200
        
        
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        db.session.add(TokenBlocklist(jti=jti))
        db.session.commit()

        return {"message": "Successfully logged out."}, 200
    
    
    
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        
        return user


    @jwt_required()
    @admin_required
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        
        db.session.delete(user)
        db.session.commit()
        
        return {"message": "User deleted."}, 200
    
    
@blp.route("/promote/<int:user_id>")
class AdminUser(MethodView):
    @jwt_required()
    @admin_required
    @blp.response(200, UserSchema)
    def put(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        
        user.is_admin = True
        
        db.session.commit()
        return {"message": f"{user.username} has been promoted to admin."}, 200
    
    
@blp.route("/demote/<int:user_id>")
class DemoteUser(MethodView):
    @jwt_required()
    @admin_required
    @blp.response(200, UserSchema)
    def put(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        if not user.is_admin:
            return {"message": f"{user.username} is not an admin."}, 400
        
        jwt = get_jwt()
        if jwt.get("sub") == str(user.id):
            return {"message": "Admin users cannot demote themselves."}, 400

        user.is_admin = False
        
        db.session.commit()
        return {"message": f"{user.username} has been demoted from admin."}, 200
    
