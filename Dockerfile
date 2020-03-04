# FROM tiangolo/uwsgi-nginx-flask:python3.7
FROM python:3.7.6-stretch

# set up working dir:
RUN mkdir /app
WORKDIR /app

# install dependencies:
COPY ${PWD}/service/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# add application:
ADD ${PWD}/service /app/

# set environment variables:
ENV LOG_LEVEL INFO
ENV FLASK_APP main.py
ENV FLASK_DEBUG true
ENV FLASK_CONFIG development
ENV STATIC_PATH /app/application/static

# launch gunicorn:
EXPOSE 8080
CMD gunicorn -b 0.0.0.0:8080 -w 2 main:app

