FROM python:3.11-buster
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r ./requirements.txt
COPY manage.py .
COPY src ./src