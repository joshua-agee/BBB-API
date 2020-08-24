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
#get comments by recipe id
@comment.route("/recipe/<recipe_id>", methods=["GET"])
def get_recipe_comments(recipe_id):
    try:
        # comments = models.Comment.select().where(models.Comment.on_recipe == recipe_id)
        comments = {}
        data = [model_to_dict(comment) for comment in models.Comment.select(models.Comment.id, models.Comment.title, models.Comment.comment, models.Comment.by_user).where(models.Comment.on_recipe == recipe_id).objects()]
        print(type(data))
        for comment in data:
            key = comment['id']
            comments[key] = comment
            print(comment, type(comment))
        print('Comments: ', comments)
        return jsonify(data=comments, status={"code": 200, "message":"success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

# get one comment by id
@comment.route("/<id>", methods=["GET"])
def get_one_comment(id):
    try:
        comment = models.Comment.get_by_id(id)
        return jsonify(data=model_to_dict(comment), status={"code": 200, "message": "success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message":"That id does not exist"})

#create new comment
@comment.route("/", methods=["POST"])
def create_comment():
    payload = request.get_json()
    print(payload)
    payload["by_user"] = current_user.id 
    new_comment = models.Comment.create(**payload)
    comment_data = model_to_dict(new_comment)
    return jsonify(data=comment_data, status={"code": 200, "message": "Success"})

#edit comment
@comment.route("/<id>", methods=["PUT"])
def update_comment(id):
    payload = request.get_json()
    print(payload)
    payload["by_user"] = current_user.id
    try:
        update_query = models.Comment.update(**payload).where(models.Comment.id == id, models.Comment.by_user == current_user.id)
        update_query.execute()
        return jsonify(
            data=model_to_dict(models.Comment.get_by_id(id)),
            status={"code" : 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message":"Comments can only be updated by submitter"})

#delete comment
@comment.route("/<id>", methods=["DELETE"])
def delete_comment(id):
    try:
        delete_query = models.Comment.delete().where(models.Comment.id == id, models.Comment.by_user == current_user.id)
        delete_query.execute()
        return jsonify(data={}, status={"code": 200, "message": "success"})
    except model.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "does not exist or not allowed by current user"})
