# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code1/
COPY requirements.txt /code1/
COPY ./manage.py /code1/
RUN pip install -r requirements.txt
COPY . /code1/

EXPOSE 8001
CMD python manage.py runserver