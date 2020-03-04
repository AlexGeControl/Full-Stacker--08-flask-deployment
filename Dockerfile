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

# launch gunicorn:
EXPOSE 8080
CMD gunicorn -b 0.0.0.0:8080 -w 2 main:app

