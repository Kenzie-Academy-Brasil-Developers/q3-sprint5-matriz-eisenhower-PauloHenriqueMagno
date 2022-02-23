from dataclasses import dataclass
from flask import current_app
from app.configs.database import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

@dataclass
class Eisenhower(db.Model):
  __tablename__ = "Eisenhowers"

  id: int = Column(Integer, primary_key = True)
  type: str = Column(String(100))

  task = relationship("Task", backref = "classification", uselist = False)

  @staticmethod
  def get_classification(importance: int, urgency: int):
    """
      Get eisenhower id from importance e urgency
    """

    if importance == 1 and urgency == 1:
      return 1
    if importance == 1 and urgency == 2:
      return 2
    if importance == 2 and urgency == 1:
      return 3
    if importance == 2 and urgency == 2:
      return 4

  @staticmethod
  def load_eisenhower():  
    if len(Eisenhower.query.all()) == 0:
      classifications = ["Do It First", "Delegate It", "Schecule It", "Delete It"]

      for classification in classifications:
        data_eisenhower = {"type": classification}
        new_eisenhower = Eisenhower(**data_eisenhower)
        
        current_app.db.session.add(new_eisenhower)
        current_app.db.session.commit()