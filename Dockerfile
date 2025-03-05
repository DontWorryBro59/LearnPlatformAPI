FROM ubuntu:latest
MAINTAINER Pertsev Sergey
LABEL authors="pertsev.sergey@gmail.com"
RUN apt-get update && \
    apt-get install -y python3.12 python3-pip && \
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
ENV DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=psql_for_app
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_TEST_NAME=psql_for_app_test

COPY /myapp /app/myapp
COPY /pytest.ini /app/pytest.ini
COPY /test_app/ /app/test_app

ENTRYPOINT ["python3", "-m", "pytest", "-v"]
ENTRYPOINT ["python3", "/myapp/main.py"]
