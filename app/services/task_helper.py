from app.models.categories_model import Category
from app.models.tasks_model import Task
from flask import current_app

def create_and_save_categories(categories: list, task: Task):
  for category in categories:
    category_name = category.lower()
    category: Category = Category.query.filter_by(name = category_name).one_or_none()

    if not category:
      category_body = {"name": category_name}
      category = Category(**category_body)

      current_app.db.session.add(category)
      current_app.db.session.commit()  

    task.categories.append(category)

def remove_categories(categories: list, task: Task):
  new_categories_lower = []
  for category in categories:
    new_categories_lower.append(category.lower())

  for task_category in task.categories:
    if task_category.name not in new_categories_lower:
      category: Category = Category.query.filter_by(name = task_category.name).one_or_none()
      task.categories.remove(category)