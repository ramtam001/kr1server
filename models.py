from pydantic import BaseModel

class UserData(BaseModel):
    name: str
    id: int