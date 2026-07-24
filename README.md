Название проекта: "Блог".
-
Краткое описание: Веб-приложение для публикации статей, новостей или заметок.

Инструкция по запуску:

Первые шаги: Установите менеджер пакетов UV и утилиту Make, если не установлены.

- Инструкция по установке UV, тут: https://docs.astral.sh/uv/getting-started/installation/

- Установка Make через терминал:
```
# Windows (powershell)

winget install ezwinports.make
```

```
# MacOS (bash)
# Установка Homebrew (если не установлен)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установка Make
brew install make

# Проверка
make --version
```
Далее

1. Скачать репозиторий
2. Открыть терминал и перейти в корень проекта скаченного репозитория
3. Выполни последовательно команды:
```bash
# установка python версии 3.12
uv python install 3.12

# установка всех зависимостей проекта
uv sync
```
4. Настрой переменные окружения
```bash
cp .env.example .env
# Открой .env и измени значение ключа SECRET_KEY
# Остальные значения из .env.example подойдут для локального старта
```
5. Установи/запусти программу Docker, затем создай Docker-контейнер с помощью команды в терминале: ```make create_docker_container```
6. Убедитесь, что контейнер активен ```docker ps``` и примени миграции: ```make migrate```
7. Загрузите данные из дампа: ```uv run manage.py loaddata datadump.json```

Ознакомьтесь с доступными командами ```make``` в файле ```Makefile```.
```bash
# Запуск сервера
make run
```
