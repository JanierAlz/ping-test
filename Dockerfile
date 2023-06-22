# syntax=docker/dockerfile:1

FROM python:3.10.12-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "--app", "flaskr", "run", "--host=0.0.0.0"]