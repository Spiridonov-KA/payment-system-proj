# Payment System

Учебный проект: система оплаты с поддержкой повторных попыток и уведомлениями.

## Технологии
- FastAPI
- SQLAlchemy + SQLite
- APScheduler (фоновые задачи)
- Pydantic (валидация)
- Mock YooMoney gateway

## Установка
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
# Создать .env при необходимости (см. .env.example)
uvicorn app.main:app --reload
```

## Тесты
```bash
pytest tests/ -v
```

## Эндпоинты

- POST /payments/ — создать платёж
- GET /payments/ — список всех платежей
- GET /payments/{id} — детали платежа
- POST /payments/{id}/refund — возврат успешного платежа
- GET /health — проверка работоспособности

## Уведомления

Все события записываются в файл `notifications.log` в корне проекта.