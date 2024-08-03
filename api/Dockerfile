FROM python:3.11.7-bullseye

WORKDIR /back-api

COPY ./requirements.txt /back-api/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /back-api/requirements.txt

COPY ./run.py /back-api/run.py

CMD ["uvicorn", "run:app", "--reload", "--host", "0.0.0.0", "--port", "80"]