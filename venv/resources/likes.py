import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

like = Blueprint("likes", "like", url_prefix="/like")


# add a like from the current user
@like.route("/", methods=["POST"])
def like_recipe():
    payload = request.get_json()
    new_like = models.Like.create(by_user=current_user.id, on_recipe=payload["recipe_id"])
    like_data=model_to_dict(new_like)
    return jsonify(data=like_data, status={"code": 200, "message":"Success"})
