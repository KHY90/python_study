# Python 이미지
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY . .

# 종속성 설치
RUN pip install --no-cache-dir fastapi sqlalchemy pymysql python-dotenv "uvicorn[standard]"
RUN pip install cryptography

# 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]