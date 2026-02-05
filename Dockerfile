FROM tensorflow/tensorflow:2.18.0

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install --default-timeout=1000 -r requirements.txt

# Run API
CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8080"]

