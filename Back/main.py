from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# MySQL 데이터베이스 연결 설정
DATABASE_URL = "mysql+pymysql://coutertest:coutertest@localhost/counter_db"
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
    return {"값": number.value}

# 숫자를 증가시키는 API
@app.post("/plus")
def plus_number():
    db = SessionLocal()
    number = db.query(Number).first()
    if not number:
        raise HTTPException(status_code=404, detail="Number not found")
    number.value += 1
    db.commit()
    return {"값": number.value}

# 숫자를 감소시키는 API
@app.post("/minus")
def minus_number():
    db = SessionLocal()
    number = db.query(Number).first()
    if not number:
        raise HTTPException(status_code=404, detail="Number not found")
    number.value -= 1
    db.commit()
    return {"값": number.value}
