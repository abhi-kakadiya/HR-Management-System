from database import db
from flask import jsonify
from flask.views import MethodView
from models.model import UserModel
from passlib.hash import pbkdf2_sha256
from flask_smorest import abort, Blueprint
from schemas.user_schema import CreateUser, AuthSchema, DisplayUser, Updateuser
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

blp = Blueprint("User", __name__, description="Operation for User")


@blp.route("/register")
class UserRegister(MethodView):

    @jwt_required()
    @blp.arguments(CreateUser)
    @blp.response(201, DisplayUser)
    def post(self, user_data):

        current_user_id = get_jwt_identity()
        if UserModel.query.filter_by(name=user_data["name"], role=user_data["role"]).first():
            abort((
                jsonify(400, message="A user with that username already exists.")))

        if UserModel.query.filter_by(id=current_user_id, role="ADMIN").first():
            newUser = UserModel(
                name=user_data["name"],
                password=pbkdf2_sha256.hash(user_data["password"]),
                email=user_data["email"],
                role=user_data["role"]
            )
            print(newUser)
            db.session.add(newUser)
            db.session.commit()
            return newUser
        else:
            abort(jsonify(code=401, message="Admin access required!"))



@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(AuthSchema)
    def get(self, user_data):

        AuthUser = UserModel.query.filter_by(email=user_data["email"]).first()
        UserBool = AuthUser and pbkdf2_sha256.verify(user_data["password"], AuthUser.password)

        if UserBool:
            admin_access_token = create_access_token(identity=AuthUser.id)
            return {"admin_access_token": admin_access_token, "token_type": "bearer"}

        else:
            abort(jsonify(code=401, message="Admin access required!"))



@blp.route("/user/<int:user_id>")
class UserApi_UD(MethodView):

    @jwt_required()
    @blp.response(200, DisplayUser)
    def get(self, user_id):

        current_user_id = get_jwt_identity()

        if UserModel.query.filter_by(id=current_user_id, role="ADMIN").first():
            user = UserModel.query.filter_by(id=user_id).first()
            if user:
                return user
            else:
                abort(jsonify(code=404, message=f"User with id {user_id} not found"))
        else:
            abort(jsonify(code=401, message="Admin access required!"))



    @jwt_required()
    @blp.arguments(Updateuser)
    @blp.response(201, DisplayUser)
    def put(self, user_data, user_id):

        current_user_id = get_jwt_identity()

        if UserModel.query.filter_by(id=current_user_id, role="ADMIN").first():
            user = UserModel.query.filter_by(id=user_id).first()
            if user:
                UserModel.query.filter_by(id=user_id).update(user_data)
                db.session.commit()
                updated_user = UserModel.query.get(user_id)
                return updated_user
            else:
                abort(jsonify(code=404, message=f"User with id {user_id} not found"))
        else:
            abort(jsonify(code=401, message="Admin access required!"))



    @jwt_required()
    def delete(self, user_id):

        current_user_id = get_jwt_identity()

        if UserModel.query.filter_by(id=current_user_id, role="ADMIN").first():
            allAdmin = UserModel.query.filter_by(role="ADMIN").all()
            if len(allAdmin) <= 1:
                user = UserModel.query.filter_by(
                    id=user_id, role="ADMIN").first()
                if user:
                    abort(jsonify(code=400, message="At least one admin must be present"))
                else:
                    user = UserModel.query.filter_by(id=user_id).first()
                    db.session.delete(user)
                    db.session.commit()
                    return {"message": f"User with id {user_id} deleted successfully"}

            else:
                user = UserModel.query.filter_by(id=user_id).first()
                if user:
                    db.session.delete(user)
                    db.session.commit()
                    return {"message": f"User with id {user_id} deleted successfully"}
                else:
                    abort(jsonify(code=404, message=f"User with id {user_id} not found"))

        else:
            abort(jsonify(code=401, message=f"Admin access required!"))