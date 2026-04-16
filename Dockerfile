FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo "DATABASE_URL=sqlite:///./payments.db" > .env
RUN echo "NOTIFICATION_FILE=notifications.log" >> .env
RUN echo "RETRY_DELAY_HOURS=24" >> .env
RUN echo "SCHEDULER_INTERVAL_MINUTES=1" >> .env

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]