FROM python:3.11.7-bullseye


WORKDIR /back-api


RUN apt-get update && apt-get install -y tzdata


ENV TZ=Europe/Madrid


RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata


COPY requirements.txt /back-api/requirements.txt


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /back-api/requirements.txt

RUN pip list


CMD ["uvicorn", "run:app", "--reload", "--host", "0.0.0.0", "--port", "80"]