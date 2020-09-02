FROM python:3.8.5

WORKDIR /code

COPY . /code

RUN apt update -y && apt install netcat -y

RUN pip install -r /code/requirements.txt

ENTRYPOINT ["/code/entrypoint.sh"]

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000