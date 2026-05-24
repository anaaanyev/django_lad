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
3. Выполнить команду для установки всех зависимостей проекта:```uv sync```

Запуск сервера: ```uv run manage.py runserver``` или ```make run```.\
Ознакомьтесь с доступными командами ```make``` в файле ```Makefile```.
