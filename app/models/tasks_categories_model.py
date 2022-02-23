from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey

@dataclass
class Tasks_categories(db.Model):
  __tablename__ = "Tasks_categories"

  id: int = Column(Integer, primary_key = True)
  
  task_id: int = Column(Integer, ForeignKey("Tasks.id"))
  category_id: int = Column(Integer, ForeignKey("Categories.id"))