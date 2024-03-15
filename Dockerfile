FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8000
ENV UVICORN_WORKERS=5

CMD uvicorn src.main:app --host $UVICORN_HOST --port $UVICORN_PORT --workers $UVICORN_WORKERS