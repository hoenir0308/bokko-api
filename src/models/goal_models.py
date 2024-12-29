from pydantic import BaseModel
from datetime import datetime

class GoalModel(BaseModel):
    title: str
    description: str
    deadline: datetime

class TaskModel(BaseModel):
    title: str
    description: str
    complite: bool
    deadline: datetime
    end_date: datetime
