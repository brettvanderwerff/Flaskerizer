FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN rm /app/*
COPY requirements.txt /app
COPY app.py /app
COPY uwsgi.ini /app
COPY static /app/static
COPY templates /app/templates
RUN pip install -r requirements.txt
