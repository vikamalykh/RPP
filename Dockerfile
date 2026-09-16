# первая стадия - сперва сборка зависимостей
FROM python:3.11-slim AS builder

WORKDIR /app

# сначала копирую только requirements.txt
COPY requirements.txt .

# зависимости в отдельную папку
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# вторая стадия - финальный образ
FROM python:3.11-slim

WORKDIR /app

# собираю установленные зависимости из стадии builder
COPY --from=builder /install /usr/local

# код приложения
COPY app.py .

# переменные окружения (значения по умолчанию)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# задокументировала порт
EXPOSE 5000

# точка входа — gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]