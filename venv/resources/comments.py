import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

comment = Blueprint("comments",  "comment", url_prefix="/comment")

#get all comments
@comment.route("/", methods=["GET"])
def get_all_comments():
    try:
        comments =[model_to_dict(comment) for comment in models.Comment.select()]
        print(comments)
        return jsonify(data=comments, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

#create new comment
@comment.route("/", methods=["POST"])
def create_comment():
    payload = request.get_json()
    print(payload)
    payload["by_user"] = current_user.id 
    new_comment = models.Comment.create(**payload)
    comment_data = model_to_dict(new_comment)
    return jsonify(data=comment_data, status={"code": 200, "message": "Success"})