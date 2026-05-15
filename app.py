from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
import re

app = FastAPI()



@app.get("/")
def home():
    return {"message": "Авторелоад действительно работает"}




@app.get("/html")
def get_html():
    return FileResponse("index.html")




@app.post("/calculate")
def calculate(num1: int, num2: int):
    result = num1 + num2
    return {"result": result}




from models import UserData

user = UserData(
    name="Иван Иванов",
    id=1
)

@app.get("/users")
def get_user():
    return user




class User(BaseModel):
    name: str
    age: int

@app.post("/user")
def check_user(user: User):

    is_adult = user.age >= 18

    return {
        "name": user.name,
        "age": user.age,
        "is_adult": is_adult
    }




feedbacks = []

class Feedback(BaseModel):

    name: str = Field(min_length=2, max_length=50)

    message: str = Field(min_length=10, max_length=500)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value):

        bad_words = ["кринж", "рофл", "вайб"]

        for word in bad_words:

            if re.search(word, value.lower()):
                raise ValueError("Использование недопустимых слов")

        return value


@app.post("/feedback")
def create_feedback(feedback: Feedback):

    feedbacks.append(feedback)

    return {
        "message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."
    }