# Официальный базовый образ Python 3.12 с предустановленным uv от Astral
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Переменные окружения для оптимизации Python и uv
ENV UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Рабочая директория приложения
WORKDIR /app

# Копируем манифесты зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем только продакшен-зависимости (слой кэшируется)
RUN uv sync --frozen --no-dev

# Копируем исходный код проекта
COPY . .

# Документируем порт
EXPOSE 8000

# Запуск Django на 0.0.0.0:8000
CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
