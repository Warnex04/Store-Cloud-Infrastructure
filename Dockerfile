FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip install confluent_kafka pymongo

CMD ["python", "kafka.py"]
