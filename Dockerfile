# syntax=docker/dockerfile:1
FROM python:3.9.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN adduser --system --group app
USER app

WORKDIR /app

RUN pip3 install --upgrade pip
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY . /app/

EXPOSE 8000