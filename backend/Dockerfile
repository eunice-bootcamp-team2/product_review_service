# Python 버전
FROM python:3.12-slim

# 작업 디렉토리
WORKDIR /app

# 시스템 패키지
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# requirements 먼저 복사
COPY requirements.txt .

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 전체 코드 복사
COPY . .

# 포트
EXPOSE 8000
