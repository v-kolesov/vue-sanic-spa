FROM python:3.6.7-slim-stretch

WORKDIR /app

RUN apt-get update

RUN apt-get -y install gcc

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

VOLUME [ "/app" ]

EXPOSE 8000

CMD ["python", "run.py"] 