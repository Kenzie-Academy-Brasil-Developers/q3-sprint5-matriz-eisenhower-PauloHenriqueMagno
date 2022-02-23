from flask import  Blueprint
from app.controllers import categories_controller

bp_categories = Blueprint("Categories", __name__, url_prefix = "")

bp_categories.get("/")(categories_controller.get_categories)
bp_categories.patch("/categories/<id>")(categories_controller.modify_category)
bp_categories.post("/categories")(categories_controller.create_category)
bp_categories.delete("/categories/<id>")(categories_controller.delete_category)