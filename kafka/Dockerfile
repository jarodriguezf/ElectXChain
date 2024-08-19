FROM python:3.11.7-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY consumer.py .

CMD ["python", "consumer.py"]