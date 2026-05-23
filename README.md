# SkySound Search API

FastAPI сервер для поиска и скачивания музыки с skysound7.com.

## Эндпоинты

- `GET /search?q=запрос` — поиск песен
- `GET /track-url?url=страница_трека` — получить download/stream URL
- `GET /stream?url=stream_url` — стриминг аудио
- `GET /download?url=download_url` — скачать mp3

## Деплой на Render

1. Залить код на GitHub
2. В Render → New Web Service → Connect repo
3. Render сам найдёт `render.yaml`
4. Готово!
