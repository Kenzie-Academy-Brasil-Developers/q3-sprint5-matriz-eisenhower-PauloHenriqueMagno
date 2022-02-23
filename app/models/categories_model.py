from app.configs.database import db
from sqlalchemy import Column, Integer, String, Text
from dataclasses import dataclass
from psycopg2.errors import InvalidParameterValue

@dataclass
class Category(db.Model):
  __tablename__ = "Categories"

  id: int = Column(Integer, primary_key = True)
  name: str = Column(String(100), nullable = False, unique = True)
  description: str = Column(Text, default = "")

  def check_category_data(data: dict):
    """
      Check category data.
    """
    valid_keys = ["name", "description"]
    invalid_keys = []
    invalid_values = {}
    valid_values = {}

    for key, value in data.items():
      if key not in valid_keys:
        invalid_keys.append(key)
      if type(value) != str:
        invalid_values[key] = value
        valid_values[key] = "str"
      if type(value) == str:
        data[key] = value.lower()

    if len(invalid_keys) > 0:
      raise KeyError({"msg": {
        "valid_options": valid_keys,
        "recieved_options": invalid_keys
      }})

    if len(invalid_values) > 0:
      raise InvalidParameterValue({"msg": {
        "valid_options": valid_values,
        "recieved_options": invalid_values
      }})