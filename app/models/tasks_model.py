from dataclasses import dataclass
from app.configs.database import db
from psycopg2.errors import NotNullViolation, InvalidParameterValue
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.models.eisenhower_model import Eisenhower
from app.models.categories_model import Category

@dataclass
class Task(db.Model):
  __tablename__ = "Tasks"

  id: int = Column(Integer, primary_key = True)
  name: str = Column(String(100), nullable = False, unique = True)
  description: str = Column(Text, default = "")
  duration: int = Column(Integer, default = 0)
  importance: int = Column(Integer, default = 1)
  urgency: int = Column(Integer, default = 1)
  eisenhower_id: int = Column(Integer, ForeignKey(Eisenhower.id), nullable = False)
  
  categories: Category = relationship("Category", secondary = "Tasks_categories", backref = "tasks")

  @staticmethod
  def check_task_data(data: dict, check_required_key = False):
    """
      Check task data.
      If a key, value type or value do not pass in any verification it will raise an Error.
    """

    required_keys: list = ["name", "categories"]
    missing_required_keys: list = ["name", "categories"]
    valid_values_type: dict = {"name": "str", "description": "str", "duration": "int", "importance": "int", "urgency": "int", "categories": "list"}
    valid_values: dict = {"importance": [1,2], "urgency": [1,2]}
    valid_keys: list = ["name", "description", "duration", "importance", "urgency", "categories"]
    msg_valid_values = {}
    invalid_values_type: dict = {}
    invalid_values: dict = {}
    invalid_keys: list = []

    #check keys, values and types
    for key, value in data.items():
      value_type = str(type(value))[8:-2]
      
      if key in required_keys and check_required_key:
        missing_required_keys.remove(key)

      if key not in valid_keys:
        invalid_keys.append(key)

      if value_type != valid_values_type.get(key):
        invalid_values_type[key] = value_type

      if valid_values.get(key) and not value in valid_values[key]:
        invalid_values[key] = value
        msg_valid_values[key] = valid_values[key]

    if type(data.get("categories")) == list and len(data.get("categories")) == 0:
      invalid_values["categories"] = data["categories"]
      msg_valid_values["categories"] = ["category_name"]

    #raise Errors

    #Required Key Error
    if len(missing_required_keys) > 0 and check_required_key:
      raise NotNullViolation({"msg": {
        "required_keys": required_keys,
        "missing_required_keys": missing_required_keys
      }})

    #Key Error
    if len(invalid_keys) > 0:
      raise KeyError({"msg": {
        "valid_options": valid_keys,
        "recieved_options": invalid_keys
      }})

    #Type Error
    if len(invalid_values_type) > 0:
      raise InvalidParameterValue({"msg": {
        "valid_options": valid_values_type,
        "recieved_options": invalid_values_type
      }})

    #Values Error
    if len(invalid_values) > 0:
      raise InvalidParameterValue({"msg": {
        "valid_options": msg_valid_values,
        "recieved_options": invalid_values
      }})