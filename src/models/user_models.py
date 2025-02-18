from pydantic import BaseModel

class UserModel(BaseModel):
    first_name: str
    last_name: str
    gender: str 
    age: int
    post: str