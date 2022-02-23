from flask import Blueprint
from app.controllers import tasks_controller

bp_tasks = Blueprint("Tasks", __name__, url_prefix = "/tasks")

bp_tasks.patch("<id>")(tasks_controller.modify_task)
bp_tasks.post("")(tasks_controller.create_task)
bp_tasks.delete("<id>")(tasks_controller.delete_task)