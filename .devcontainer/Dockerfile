# Dev Dockerfile

# 베이스 이미지 선택
FROM python:3.8
USER root

# apt-get 업데이트 및 기본 패키지 설치
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    && apt-get install -y nodejs \
    && apt-get install -y npm \
    && pip install --upgrade pip

# # Node.js 설치
# RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
# RUN apt-get install -y nodejs
    
# # npm 최신 버전으로 업데이트
# RUN npm install -g npm

# 작업 디렉토리 설정
WORKDIR /container

# Python 패키지 설치
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Node.js 패키지 설치
COPY package.json .
RUN npm install

# Port 명시
EXPOSE 8080
EXPOSE 5173

# 도커 시작 명령
CMD ["bash"]
