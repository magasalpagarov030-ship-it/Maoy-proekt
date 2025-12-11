from fastapi import FastAPI, HTTPException
from database import Base, engine, SessionLocal
from models import User
from utils import generate_code, send_code_to_group
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/send_code")
def send_code(phone: str):
    db = SessionLocal()

    code = generate_code()

    user = db.query(User).filter(User.phone == phone).first()

    if not user:
        user = User(phone=phone, code=code)
        db.add(user)
    else:
        user.code = code

    db.commit()

    sent = send_code_to_group(code, phone)

    if not sent:
        raise HTTPException(status_code=500, detail="Не удалось отправить код в Telegram")

    return {"message": "Код отправлен"}


@app.post("/login")
def login(phone: str, code: str):
    db = SessionLocal()

    user = db.query(User).filter(User.phone == phone, User.code == code).first()

    if not user:
        raise HTTPException(status_code=400, detail="Неверный код")

    token = jwt.encode({"phone": phone}, SECRET_KEY, algorithm="HS256")

    return {"token": token}
