FROM python:3.11-buster
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt
COPY main.py .
COPY src ./src