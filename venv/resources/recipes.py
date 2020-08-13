import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required
from peewee import *

recipe = Blueprint("recipes", "recipe")

# Get all recipes
@recipe.route("/", methods=["GET"])
def get_all_recipes():
    try:
        # add likes and comments lookup here?
        # recipes = [model_to_dict(recipe, recipe.likes) for recipe 
        #     in models.Recipe.select(models.Recipe,
        #     fn.COUNT(models.Like.id).alias('likes'))
        #     .join(models.Like, JOIN.LEFT_OUTER)
        #     .group_by(models.Recipe)]
        # print(recipes)
        query = models.Recipe.select(models.Recipe, fn.COUNT(models.Like.on_recipe).alias('likes'), fn.COUNT(models.Comment.on_recipe).alias('comments')).join(models.Like, JOIN.LEFT_OUTER).switch(models.Recipe).join(models.Comment, JOIN.LEFT_OUTER).group_by(models.Recipe.id).order_by(models.Recipe.id)
        recipes = [model_to_dict(recipe) for recipe in query.objects()]
        for recipe in query:
            print(recipe.name, recipe.likes, recipe.comments)
            # recipes[recipe]["num_likes"] = recipe.likes
            # recipes[recipe]["num_comments"] = recipe.comments
        # return jsonify(data=model_to_dict(query), status={"code": 200, "message": "Success"})
        return jsonify(recipes=recipes, status={"code": 200, "message":"success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

# Create a new recipe
@recipe.route("/", methods=["POST"])
def create_recipe():
    payload = request.get_json()
    print(payload)
    payload["contributor_id"] = current_user.id
    new_recipe = models.Recipe.create(**payload)
    recipe_data = model_to_dict(new_recipe)
    return jsonify(data=recipe_data, status={"code": 200, "message":"Success"})

# Get one recipe by id
@recipe.route("/<id>", methods=["GET"])
def get_one_recipe(id):
    try:
        recipe = models.Recipe.get_by_id(id)
        recipe_dict = model_to_dict(recipe)
        likes = models.Like.select().where(models.Like.on_recipe == id).count()
        return jsonify(data=recipe_dict, likes=likes, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message":"That id does not exist"})

# Update recipe
@recipe.route("/<id>", methods=["PUT"])
def update_recipe(id):
    payload = request.get_json()
    update_query = models.Recipe.update(**payload).where(models.Recipe.id == id)
    update_query.execute()
    return jsonify(
        data=model_to_dict(models.Recipe.get_by_id(id)), 
        status={"code":200, "message": "record update"})

#like recipe toggle
@recipe.route("/<id>/like", methods=["POST"])
def toggle_like_recipe(id):
    try:
        like = models.Like.get(models.Like.on_recipe==id, models.Like.by_user==current_user.id)
        like.delete_instance()
        return jsonify(data={}, status={"code": 200, "message": "unliked"})
    except models.DoesNotExist:
        like = models.Like.create(on_recipe=id, by_user=current_user.id)
        return jsonify(data={}, status={"code": 200, "message": "liked"})


# Delete recipe
@recipe.route("/<id>", methods=["DELETE"])
def delete_recipe(id):
    delete_query = models.Recipe.delete().where(models.Recipe.id == id)
    delete_query.execute()
    return jsonify(
        data={},
        message="Successfully deleted recipe with id {}".format(id),
        status= 200
    )