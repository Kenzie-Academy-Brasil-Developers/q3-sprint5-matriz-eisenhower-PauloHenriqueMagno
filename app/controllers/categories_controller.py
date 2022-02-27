from flask import current_app, jsonify, request
from app.models.categories_model import Category
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from psycopg2.errors import InvalidParameterValue

def get_categories():
  categories = Category.query.all()
  categories_list = []

  for category in categories:
    categories_list.append(
      {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "tasks": [ 
          {
          "id": task.id,
          "name": task.name,
          "description": task.description,
          "duration": task.duration,
          "classification": task.classification.type
          } for task in category.tasks
        ]
      }
    )
  return jsonify(categories_list), 200

def create_category():
  try:
    data = request.json

    Category.check_category_data(data)

    categorie = Category(**data)

    current_app.db.session.add(categorie)
    current_app.db.session.commit()

    return jsonify(categorie), 201

  except IntegrityError as err:
    return jsonify({"msg": "category already exists!"}), 409

  except KeyError as err:
    return jsonify(err.args[0]), 400
  
  except InvalidParameterValue as err:
    return jsonify(err.args[0]), 400

def delete_category(id: int):
  try:
    category = Category.query.get_or_404(id)

    current_app.db.session.delete(category)
    current_app.db.session.commit()

    return jsonify(), 204
    
  except NotFound:
    return jsonify({"error": "category not found!"}), 404

def modify_category(id: int):
  data: dict = request.json

  try:
    category = Category.query.get_or_404(id)

    Category.check_category_data(data)

    for key, value in data.items():
      setattr(category, key, value)

    current_app.db.session.add(category)
    current_app.db.session.commit()

    return jsonify(category), 200

  except NotFound:
    return jsonify({"msg": "category not found"}), 404