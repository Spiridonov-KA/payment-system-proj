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

## Конфигурация (.env)

| Переменная | Значение по умолчанию | Описание |
|------------|----------------------|----------|
| `DATABASE_URL` | `sqlite:///./payments.db` | Строка подключения к БД |
| `NOTIFICATION_FILE` | `/app/logs/notifications.log` | Путь к файлу логов уведомлений |
| `RETRY_DELAY_HOURS` | `24` | Через сколько часов повторять неудачный платёж |
| `SCHEDULER_INTERVAL_MINUTES` | `1` | Как часто планировщик проверяет просроченные платежи |

## Запуск

```bash
# Создать .env при необходимости (см. .env.example)
uvicorn app.main:app --reload
```

## Запуск через Docker

```bash
# Создать папку для логов (чтобы Docker не создал директорию вместо файла)
mkdir -p logs

# Сборка и запуск
docker compose up --build -d

# Просмотр логов приложения
docker compose logs -f payment-api

# Остановка
docker compose down
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