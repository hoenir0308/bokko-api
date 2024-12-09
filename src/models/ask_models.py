from pydantic import BaseModel

class MotivationModel(BaseModel):
    emotional: int
    promt: str