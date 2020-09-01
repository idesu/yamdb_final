FROM python:latest

RUN mkdir /code

COPY requirements.txt /code

RUN apt update -y && apt install netcat -y

RUN pip install -r /code/requirements.txt

COPY . /code
COPY ./entrypoint.sh .
WORKDIR /code

ENTRYPOINT ["/code/entrypoint.sh"]

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000