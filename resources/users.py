import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict

user = Blueprint("users", "user", url_prefix="/user")

# This route is for user registration
@user.route("/register", methods=["POST"])
def register():
    payload = request.get_json()
    print(payload)
    payload["email"] = payload["email"].lower()
    try:
        models.User.get(models.User.email == payload["email"])
        return jsonify(data={}, status={"code":401, "message": "A user with this email already exists"})
    except models.DoesNotExist:
        payload["password"] = generate_password_hash(payload["password"])
        user = models.User.create(**payload)

        login_user(user)

        user_dict = model_to_dict(user)
        print(user_dict)
        del user_dict["password"]

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

# Login route
@user.route("/login", methods=["POST"])
def login():
    payload = request.get_json()
    payload["email"] = payload["email"].lower()
    try:
        user = models.User.get(models.User.email == payload["email"])
        user_dict = model_to_dict(user)
        if (check_password_hash(user_dict["password"], payload["password"])):
            del user_dict["password"]
            login_user(user)
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or password is incorrect"})

#Return current user data
@user.route("/id", methods=["GET"])
@login_required
def get_user():
    return jsonify(
        # recipes submitted by current user - backref method
        user_backref_recipes=[model_to_dict(recipe) for recipe in models.User.get(models.User.id == current_user.id).recipes],
        # current user object
        current_user_obj=model_to_dict(current_user), 
        # recipes submitted by current user - where method
        user_recipes=[model_to_dict(recipe) for recipe in models.Recipe.select().join(models.User).where(models.User.id == current_user.id)], 
        # recipes liked by current user where method
        liked_recipes=[model_to_dict(recipe) for recipe in models.Recipe.select().join(models.Like).where(models.Like.by_user == current_user.id)],
        # recipes liked by current user backref method
        liked_recipes_backref=[model_to_dict(recipe) for recipe in models.User.get(models.User.id == current_user.id).likes],
        #comments by burrent user backref method
        user_backref_comments=[model_to_dict(comment) for comment in models.User.get(models.User.id == current_user.id).comments],
        status={"code": 200, "message": "Success"})

#Logout current user
@user.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return jsonify(data={}, status={"code": 200, "message": "User logged out successfully"})