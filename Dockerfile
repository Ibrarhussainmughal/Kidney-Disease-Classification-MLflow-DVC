FROM python:3.10-slim-buster

RUN apt-get update -y && apt-get install -y awscli
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8080"]
