
# Используем официальный образ Python в качестве базового образа
FROM python:3.10-alpine3.17

RUN pip install --upgrade pip
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .