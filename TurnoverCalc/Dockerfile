# TurnoverCalc Service
FROM python:3.11.5-slim

WORKDIR /app

COPY TurnoverCalc.py requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./TurnoverCalc.py"]
