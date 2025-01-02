from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL 데이터베이스 연결 설정
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL 환경 변수가 설정되지 않았습니다.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 숫자를 저장할 테이블 모델
class Number(Base):
    __tablename__ = "numbers"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, default=0)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 숫자를 조회하는 API
@app.get("/number")
def get_number():
    db = SessionLocal()
    number = db.query(Number).first()
    if not number:
        number = Number(value=0)
        db.add(number)
        db.commit()
    return {"value": number.value}

# 숫자를 증가시키는 API
@app.post("/plus")
def plus_number():
    db = SessionLocal()
    number = db.query(Number).first()
    if not number:
        raise HTTPException(status_code=404, detail="Number not found")
    number.value += 1
    db.commit()
    return {"value": number.value}

# 숫자를 감소시키는 API
@app.post("/minus")
def minus_number():
    db = SessionLocal()
    number = db.query(Number).first()
    if not number:
        raise HTTPException(status_code=404, detail="Number not found")
    number.value -= 1
    db.commit()
    return {"value": number.value}
