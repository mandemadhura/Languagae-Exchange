# syntax=docker/dockerfile:1

FROM python:3.8
WORKDIR /Language-Exchange

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
ENV FLASK_APP=server.py

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]
