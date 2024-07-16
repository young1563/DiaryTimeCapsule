# Dev Dockerfile

# 베이스 이미지 선택
FROM python:3.8
USER root

RUN apt-get update && apt-get install -y \
    software-properties-common \
    && pip install --upgrade pip

# 작업 디렉토리 설정
WORKDIR /container

# 패키지 설치
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Port 명시
EXPOSE 8080