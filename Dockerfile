# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip install pipenv

RUN pipenv install --system --deploy --ignore-pipfile

CMD [ "python3", "modsim.py", "-p" ,"8502", "mbmap_test_device.xml" ]
