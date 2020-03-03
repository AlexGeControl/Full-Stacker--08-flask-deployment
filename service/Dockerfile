FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ${PWD}/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

ADD ${PWD} /app/