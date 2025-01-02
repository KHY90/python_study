# Node 이미지
FROM node:14

# 작업 디렉토리 설정
WORKDIR /app

# package.json 및 package-lock.json 복사
COPY package.json ./
COPY . .

# 종속성 설치
RUN npm install

# 애플리케이션 실행
CMD ["npm", "start"]
