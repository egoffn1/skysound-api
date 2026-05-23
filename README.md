# SkySound Search API

FastAPI сервер для поиска музыки на skysound7.com.

## Эндпоинты

- `GET /ping` — health check (чтобы не засыпал)
- `GET /search?q=запрос` — поиск песен
- `GET /track-url?url=страница_трека` — получить download/stream URL

## Как не дать серверу заснуть (Render free tier)

Render бесплатный тариф выключает сервер через 15 мин бездействия.

### Вариант 1: cron-job.org (рекомендую)

1. Зайди на https://cron-job.org
2. Зарегистрируйся (бесплатно)
3. Создай новый cron job:
   - **URL**: `https://твой-проект.onrender.com/ping`
   - **Interval**: Every 10 minutes (или 5)
   - **Save**
4. Готово — сервер будет просыпаться каждые 10 минут

### Вариант 2: UptimeRobot

1. Зайди на https://uptimerobot.com
2. Добавь монитор типа HTTP(s) → `https://твой-проект.onrender.com/ping`
3. Interval: 5 minutes
