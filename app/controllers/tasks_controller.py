from flask import jsonify, request, current_app
from app.models.tasks_model import Task
from app.models.eisenhower_model import Eisenhower
from app.services.task_helper import create_and_save_categories, remove_categories
from psycopg2.errors import NotNullViolation, InvalidParameterValue
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

# def get_tasks():
#   tasks = Task.query.all()

#   return jsonify(tasks), 200

def create_task():
  Eisenhower.load_eisenhower()
  data: dict = request.json
  
  try:
    Task.check_task_data(data, check_required_key = True)

    categories = data.pop("categories")
    data["importance"] = data.get("importance", 1)
    data["urgency"] = data.get("urgency", 1)
    data["eisenhower_id"] = Eisenhower.get_classification(data["importance"], data["urgency"])

    for key, value in data.items():
      if type(value) == str:
        data[key] == value.lower()

    task = Task(**data)

    create_and_save_categories(categories, task)

    current_app.db.session.add(task)
    current_app.db.session.commit()

    return jsonify({
      "id": task.id,
      "name": task.name,
      "description": task.description,
      "duration": task.duration,  
      "importance": task.importance,
      "urgency": task.urgency,
      "classification": Eisenhower.query.get(task.eisenhower_id).type,
      "categories": [ category.name for category in task.categories ]
    }), 201

  except KeyError as err:
    return jsonify(err.args[0]), 400

  except IntegrityError as err:
    return jsonify({"msg": data["name"] + " has already been taken"}), 409 

  except InvalidParameterValue as err:
    return jsonify(err.args[0]), 400

  except NotNullViolation as err:
    return jsonify(err.args[0]), 400

def delete_task(id: int):
  try:
    task = Task.query.get_or_404(id)

    current_app.db.session.delete(task)
    current_app.db.session.commit()

    return jsonify(), 204

  except NotFound:
    return jsonify({"msg": "task not found!"}), 404

def modify_task(id: int):
  Eisenhower.load_eisenhower()
  data: dict = request.json

  try:
    Task.check_task_data(data)

    task = Task.query.get_or_404(id)

    categories = [ category.name for category in task.categories ]
    categories = data.pop("categories", categories)

    for key, value in data.items():
      setattr(task, key, value)

    eisenhower_id = Eisenhower.get_classification(task.importance, task.urgency)
    setattr(task, "eisenhower_id", eisenhower_id)

    remove_categories(categories, task)

    create_and_save_categories(categories, task)

    current_app.db.session.add(task)
    current_app.db.session.commit()

    return jsonify({
      "id": task.id,
      "name": task.name,
      "description": task.description,
      "duration": task.duration,  
      "classification": Eisenhower.query.get(task.eisenhower_id).type,
      "categories": [ category.name for category in task.categories ]
    }), 201

  except KeyError as err:
    return jsonify(err.args[0]), 400

  except IntegrityError as err:
    return jsonify({"msg": data["name"] + " has already been taken"}), 409 

  except InvalidParameterValue as err:
    return jsonify(err.args[0]), 400

  except NotFound:
    return jsonify({"msg": "task not found!"}), 404