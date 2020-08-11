import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

recipe = Blueprint('recipes', 'recipe')

@recipe.route('/', methods=['GET'])
def get_all_recipes():
    try:
        recipes = [model_to_dict(recipe) for recipe in models.Recipe.select()]
        print(recipes)
        return jsonify(data=recipes, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@recipe.route('/', methods=['POST'])
def create_recipe():
    payload = request.get_json()
    print(payload)
    new_recipe = models.Recipe.create(**payload)
    recipe_data = model_to_dict(new_recipe)
    return jsonify(data=recipe_data, status={"code": 200, "message":"Success"})