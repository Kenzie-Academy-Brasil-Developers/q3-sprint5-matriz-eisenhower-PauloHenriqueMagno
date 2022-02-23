import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app: Flask):
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
  app.config['JSON_SORT_KEYS'] = False

  db.init_app(app)
  app.db = db

  #TABLES

  from app.models.categories_model import Category
  from app.models.eisenhower_model import Eisenhower
  from app.models.tasks_model import Task
  from app.models.tasks_categories_model import Tasks_categories