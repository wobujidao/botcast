# BotCast 🚀

<div align="center">
  <h3>Профессиональная система управления рассылками через Telegram ботов</h3>
  <p>
    <img src="https://img.shields.io/badge/Python-3.12-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/FastAPI-0.115-green.svg" alt="FastAPI Version">
    <img src="https://img.shields.io/badge/PostgreSQL-16-blue.svg" alt="PostgreSQL Version">
    <img src="https://img.shields.io/badge/Redis-Latest-red.svg" alt="Redis">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  </p>
</div>

## 📋 Оглавление

- [О проекте](#-о-проекте)
- [Возможности](#-возможности)
- [Архитектура](#-архитектура)
- [Технологический стек](#-технологический-стек)
- [Требования](#-требования)
- [Установка](#-установка)
- [Конфигурация](#-конфигурация)
- [Использование](#-использование)
- [API документация](#-api-документация)
- [Структура проекта](#-структура-проекта)
- [Разработка](#-разработка)
- [Тестирование](#-тестирование)
- [Деплой](#-деплой)
- [Мониторинг](#-мониторинг)
- [Дорожная карта](#-дорожная-карта)
- [Вклад в проект](#-вклад-в-проект)
- [Лицензия](#-лицензия)
- [Контакты](#-контакты)

## 🎯 О проекте

**BotCast** - это современная платформа для централизованного управления множеством Telegram ботов и автоматизации рассылок. Система позволяет управлять несколькими ботами из единого интерфейса, создавать сложные сценарии рассылок, анализировать эффективность и масштабироваться под любые задачи.

### Ключевые преимущества:

- **Мультибот поддержка**: Управляйте десятками ботов из одного места
- **Гибкие рассылки**: Сегментация аудитории, персонализация, A/B тестирование
- **Высокая производительность**: Асинхронная архитектура для обработки миллионов сообщений
- **Надежность**: Автоматическое восстановление, retry механизмы, мониторинг
- **API First**: Полноценный REST API для интеграции с внешними системами
- **Безопасность**: JWT авторизация, шифрование данных, защита от спама

## ✨ Возможности

### Реализовано ✅

- **Аутентификация и авторизация**
  - Регистрация пользователей с валидацией email
  - JWT токены для безопасной авторизации
  - Refresh токены для продления сессий
  - Хеширование паролей (bcrypt)
  
- **Управление ботами**
  - Добавление множества Telegram ботов
  - Валидация токенов через Telegram API
  - Активация/деактивация ботов
  - Получение статистики по каждому боту

- **Webhook интеграция**
  - Автоматическая регистрация подписчиков по команде /start
  - Обработка webhook запросов от Telegram
  - Отправка приветственных сообщений
  - Автоматическое обновление информации о подписчиках

- **Система рассылок**
  - Создание и запуск рассылок
  - Фоновая отправка через ARQ workers
  - Обработка ошибок и retry механизмы
  - Детальная статистика отправки

- **База данных**
  - PostgreSQL с асинхронным драйвером asyncpg
  - Миграции через Alembic
  - Оптимизированные индексы
  - Связи между таблицами

- **Инфраструктура**
  - Systemd службы для автозапуска
  - Redis для кеширования и очередей
  - Логирование всех операций
  - Метрики производительности

### В разработке 🚧

- **Расширенные возможности рассылок**
  - Шаблоны сообщений с переменными
  - Отложенные рассылки
  - Рассылки по расписанию (cron)
  - Сегментация аудитории
  
- **Веб-интерфейс**
  - React админ-панель
  - Дашборд со статистикой
  - Визуальный редактор рассылок
  - Управление подписчиками

- **Аналитика**
  - Детальная статистика доставки
  - Конверсии и вовлеченность
  - Экспорт отчетов в различных форматах
  - A/B тестирование
  
- **Интеграции**
  - Webhook для внешних систем
  - Импорт/экспорт подписчиков (CSV, Excel)
  - API для CRM систем
  - Интеграция с Google Analytics

## 🏗 Архитектура

```mermaid
graph TB
    subgraph "Frontend"
        A[React SPA] --> B[Nginx]
    end
    
    subgraph "Backend"
        B --> C[FastAPI]
        C --> D[PostgreSQL]
        C --> E[Redis]
        C --> F[ARQ Workers]
    end
    
    subgraph "External"
        F --> G[Telegram API]
        C --> H[External APIs]
    end
```

### Компоненты системы:

1. **FastAPI Backend** - Основное API приложение
2. **PostgreSQL** - Основная база данных
3. **Redis** - Кеш и брокер сообщений
4. **ARQ Workers** - Воркеры для фоновых задач
5. **Nginx** - Reverse proxy и статика
6. **React Frontend** - SPA админ-панель

## 🛠 Технологический стек

### Backend
- **Python 3.12** - Основной язык программирования
- **FastAPI** - Современный асинхронный веб-фреймворк
- **SQLAlchemy 2.0** - ORM с поддержкой async/await
- **Alembic** - Миграции базы данных
- **Pydantic** - Валидация данных
- **UV** - Быстрый менеджер пакетов Python

### База данных и кеширование
- **PostgreSQL 16** - Основная база данных
- **Redis** - Кеш и очереди сообщений
- **ARQ** - Распределенные задачи

### Telegram интеграция
- **Aiogram 3** - Асинхронная библиотека для Telegram Bot API
- **aiohttp** - HTTP клиент для внешних запросов

### Инфраструктура
- **Docker & Docker Compose** - Контейнеризация
- **Nginx** - Веб-сервер и reverse proxy
- **Systemd** - Управление службами
- **GitHub Actions** - CI/CD

## 📦 Требования

### Системные требования

- **ОС**: Ubuntu 24.04 LTS (рекомендуется) или другой Linux дистрибутив
- **CPU**: 2+ ядра
- **RAM**: 4GB минимум, 8GB рекомендуется
- **Диск**: 20GB свободного места

### Программное обеспечение

- Python 3.12+
- PostgreSQL 16+
- Redis 7+
- Git
- curl или wget

## 🚀 Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/wobujidao/botcast.git
cd botcast
```

### 2. Установка системных зависимостей

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python 3.12
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Установка PostgreSQL 16
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo tee /etc/apt/trusted.gpg.d/pgdg.asc
sudo apt update
sudo apt install -y postgresql-16 postgresql-client-16

# Установка Redis
sudo apt install -y redis-server

# Дополнительные утилиты
sudo apt install -y git curl build-essential
```

### 3. Установка UV (менеджер пакетов Python)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # или перезапустите терминал
```

### 4. Настройка PostgreSQL

```bash
# Переключаемся на пользователя postgres
sudo -u postgres psql

-- Создаем пользователя и базу данных
CREATE USER botcast_user WITH PASSWORD 'your_secure_password_here';
CREATE DATABASE botcast_db OWNER botcast_user;
GRANT ALL PRIVILEGES ON DATABASE botcast_db TO botcast_user;

-- Выход
\q
```

### 5. Настройка Redis

```bash
# Проверяем, что Redis запущен
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo systemctl status redis-server
```

### 6. Установка Python зависимостей

```bash
# Создаем виртуальное окружение
uv venv

# Устанавливаем зависимости
uv pip install -r requirements.txt
```

### 7. Настройка переменных окружения

```bash
# Копируем пример конфигурации
cp .env.example .env

# Редактируем конфигурацию
nano .env
```

Содержимое `.env` файла:

```env
# Основные настройки
APP_NAME="BotCast"
DEBUG=false
HOST=0.0.0.0
PORT=8000

# База данных
DATABASE_URL=postgresql+asyncpg://botcast_user:your_secure_password_here@localhost/botcast_db

# Redis
REDIS_URL=redis://localhost:6379

# Безопасность
SECRET_KEY=your-very-long-random-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Telegram (опционально для тестов)
TEST_BOT_TOKEN=your_test_bot_token_here
```

### 8. Применение миграций

```bash
# Инициализация базы данных
uv run alembic upgrade head
```

### 9. Первый запуск

```bash
# Запуск в режиме разработки
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Проверка работоспособности
curl http://localhost:8000/health
```

## ⚙️ Конфигурация

### Настройка systemd службы

Создайте файл `/etc/systemd/system/botcast.service`:

```ini
[Unit]
Description=BotCast API Service
After=network.target postgresql.service redis.service

[Service]
Type=exec
User=your_username
Group=your_username
WorkingDirectory=/path/to/botcast
Environment="PATH=/home/your_username/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/home/your_username/.local/bin/uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Создайте файл `/etc/systemd/system/botcast-worker.service`:

```ini
[Unit]
Description=BotCast ARQ Worker
After=network.target postgresql.service redis.service

[Service]
Type=exec
User=your_username
Group=your_username
WorkingDirectory=/path/to/botcast
Environment="PATH=/home/your_username/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/home/your_username/.local/bin/uv run arq worker.WorkerSettings
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Активация служб:

```bash
sudo systemctl daemon-reload
sudo systemctl enable botcast botcast-worker
sudo systemctl start botcast botcast-worker
sudo systemctl status botcast botcast-worker
```

### Настройка Nginx (опционально)

```nginx
server {
    listen 80;
    server_name botcast.ru www.botcast.ru;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📖 Использование

### API Endpoints

#### Аутентификация

**Регистрация пользователя**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Авторизация**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

#### Управление ботами

**Добавление бота**
```bash
curl -X POST http://localhost:8000/bots \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bot_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    "bot_name": "My Awesome Bot"
  }'
```

**Получение списка ботов**
```bash
curl -X GET http://localhost:8000/bots \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Webhook интеграция

**Настройка webhook для бота**
```bash
python setup_webhook.py YOUR_BOT_TOKEN https://yourdomain.com/telegram/webhook/YOUR_BOT_TOKEN
```

Для локального тестирования с ngrok:
```bash
# Установите ngrok
# Запустите туннель
ngrok http 8000

# Используйте URL от ngrok
python setup_webhook.py YOUR_BOT_TOKEN https://abc123.ngrok.io/telegram/webhook/YOUR_BOT_TOKEN
```

#### Управление рассылками

**Создание рассылки**
```bash
curl -X POST http://localhost:8000/broadcasts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": 1,
    "name": "Тестовая рассылка",
    "message_text": "Привет! Это тестовое сообщение."
  }'
```

**Запуск рассылки**
```bash
curl -X POST http://localhost:8000/broadcasts/{broadcast_id}/start \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Python SDK (пример)

```python
import asyncio
from botcast_sdk import BotCastClient

async def main():
    # Инициализация клиента
    client = BotCastClient(
        base_url="https://api.botcast.ru",
        api_key="your_api_key"
    )
    
    # Создание рассылки
    broadcast = await client.broadcasts.create(
        bot_id=1,
        message="Привет! Это тестовая рассылка.",
        recipients=["user_id_1", "user_id_2"],
        scheduled_at="2024-01-01 12:00:00"
    )
    
    print(f"Рассылка создана: {broadcast.id}")

asyncio.run(main())
```

## 📚 API Документация

### Swagger/OpenAPI

После запуска сервера документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI Schema: http://localhost:8000/openapi.json

### Основные разделы API

1. **Authentication** (`/auth/*`)
   - POST `/auth/register` - Регистрация
   - POST `/auth/login` - Авторизация
   - POST `/auth/refresh` - Обновление токена
   - POST `/auth/logout` - Выход

2. **Bots** (`/bots/*`)
   - GET `/bots` - Список ботов
   - POST `/bots` - Добавить бота
   - GET `/bots/{bot_id}` - Информация о боте
   - PUT `/bots/{bot_id}` - Обновить бота
   - DELETE `/bots/{bot_id}` - Удалить бота

3. **Broadcasts** (`/broadcasts/*`)
   - GET `/broadcasts` - Список рассылок
   - POST `/broadcasts` - Создать рассылку
   - GET `/broadcasts/{id}` - Детали рассылки
   - POST `/broadcasts/{id}/start` - Запустить рассылку
   - POST `/broadcasts/{id}/cancel` - Отменить рассылку
   - GET `/broadcasts/{id}/stats` - Статистика рассылки

4. **Webhook** (`/telegram/*`)
   - POST `/telegram/webhook/{bot_token}` - Webhook endpoint для Telegram

5. **Analytics** (`/analytics/*`)
   - GET `/analytics/overview` - Общая статистика
   - GET `/analytics/bots/{bot_id}` - Статистика бота
   - GET `/analytics/broadcasts/{id}` - Статистика рассылки

## 📁 Структура проекта

```
botcast/
├── app/                        # Основное приложение
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py            # Аутентификация
│   │   ├── bots.py            # Управление ботами
│   │   ├── broadcasts.py      # Рассылки
│   │   ├── webhook.py         # Webhook для Telegram
│   │   └── deps.py            # Зависимости
│   │
│   ├── core/                   # Конфигурация и утилиты
│   │   ├── __init__.py
│   │   ├── config.py          # Настройки приложения
│   │   ├── database.py        # Подключение к БД
│   │   ├── security.py        # Безопасность
│   │   └── redis.py           # Redis клиент
│   │
│   ├── models/                 # SQLAlchemy модели
│   │   ├── __init__.py
│   │   ├── base.py            # Базовая модель
│   │   ├── user.py            # Модель пользователя
│   │   ├── telegram_bot.py    # Модель бота
│   │   ├── subscriber.py      # Модель подписчика
│   │   ├── broadcast.py       # Модель рассылки
│   │   └── broadcast_message.py # Модель сообщения
│   │
│   ├── schemas/                # Pydantic схемы
│   │   ├── __init__.py
│   │   ├── user.py            # Схемы пользователя
│   │   ├── telegram_bot.py    # Схемы бота
│   │   ├── subscriber.py      # Схемы подписчика
│   │   └── broadcast.py       # Схемы рассылки
│   │
│   ├── services/               # Бизнес-логика
│   │   ├── __init__.py
│   │   ├── auth.py            # Сервис авторизации
│   │   ├── telegram.py        # Telegram интеграция
│   │   └── broadcast.py       # Сервис рассылок
│   │
│   ├── workers/                # Фоновые задачи
│   │   ├── __init__.py
│   │   └── broadcast.py       # Воркер рассылок
│   │
│   └── main.py                # Точка входа FastAPI
│
├── alembic/                    # Миграции БД
│   ├── versions/              # Файлы миграций
│   ├── alembic.ini           # Конфигурация Alembic
│   ├── env.py                # Окружение миграций
│   └── script.py.mako        # Шаблон миграций
│
├── tests/                      # Тесты
│   ├── conftest.py           # Fixtures
│   ├── test_auth.py          # Тесты авторизации
│   ├── test_bots.py          # Тесты ботов
│   └── test_broadcasts.py    # Тесты рассылок
│
├── scripts/                    # Вспомогательные скрипты
│   ├── setup_webhook.py      # Настройка webhook
│   ├── test_api.py           # Тестирование API
│   └── check_stats.py        # Проверка статистики
│
├── docs/                       # Документация
│   ├── WEBHOOK_SETUP.md      # Настройка webhook
│   └── CURRENT_STATUS.md     # Текущий статус проекта
│
├── .github/                    # GitHub конфигурация
│   └── workflows/             # CI/CD pipelines
│       ├── tests.yml         # Запуск тестов
│       └── deploy.yml        # Деплой
│
├── requirements.txt            # Python зависимости
├── requirements-dev.txt        # Dev зависимости
├── .env.example               # Пример конфигурации
├── .gitignore                 # Git игнор
├── Dockerfile                 # Docker образ
├── docker-compose.yml         # Docker Compose конфигурация
├── worker.py                  # Точка входа для ARQ воркера
├── pyproject.toml             # Конфигурация проекта
└── README.md                  # Этот файл
```

## 🔧 Разработка

### Настройка окружения разработки

```bash
# Клонирование репозитория
git clone https://github.com/wobujidao/botcast.git
cd botcast

# Создание виртуального окружения
uv venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# Установка зависимостей для разработки
uv pip install -r requirements-dev.txt

# Настройка pre-commit хуков
pre-commit install
```

### Полезные команды

```bash
# Форматирование кода
make format

# Проверка линтерами
make lint

# Запуск тестов
make test

# Создание новой миграции
make migration message="Add new table"

# Применение миграций
make migrate

# Запуск в dev режиме
make dev

# Сборка Docker образа
make build

# Полная очистка
make clean
```

### Makefile команды

```makefile
.PHONY: help
help:
    @echo "Доступные команды:"
    @echo "  make install    - Установить зависимости"
    @echo "  make dev        - Запустить в режиме разработки"
    @echo "  make test       - Запустить тесты"
    @echo "  make lint       - Проверить код линтерами"
    @echo "  make format     - Отформатировать код"
    @echo "  make migrate    - Применить миграции"
    @echo "  make build      - Собрать Docker образ"
    @echo "  make clean      - Очистить временные файлы"
```

### Стиль кода

Проект использует:
- **Black** - форматирование кода
- **isort** - сортировка импортов
- **flake8** - линтер
- **mypy** - проверка типов
- **pytest** - тестирование

Конфигурация в `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py312']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
```

## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
pytest

# С покрытием
pytest --cov=app --cov-report=html

# Только unit тесты
pytest tests/unit

# Только интеграционные тесты
pytest tests/integration

# Конкретный тест
pytest tests/test_auth.py::test_user_registration
```

### Написание тестов

Пример теста:

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_user_registration():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "testpassword123"
            }
        )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
```

### Тестовая база данных

Для тестов используется отдельная база данных, которая создается автоматически:

```python
# tests/conftest.py
@pytest.fixture
async def test_db():
    # Создание тестовой БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Очистка после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

## 🚢 Деплой

### Docker

```bash
# Сборка образа
docker build -t botcast:latest .

# Запуск контейнера
docker run -d \
  --name botcast \
  -p 8000:8000 \
  --env-file .env \
  botcast:latest
```

### Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: botcast_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: botcast_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
      
  worker:
    build: .
    command: arq worker.WorkerSettings
    depends_on:
      - db
      - redis
    env_file:
      - .env

volumes:
  postgres_data:
```

### Kubernetes

Пример deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: botcast-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: botcast-api
  template:
    metadata:
      labels:
        app: botcast-api
    spec:
      containers:
      - name: api
        image: botcast:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: botcast-secrets
              key: database-url
```

### CI/CD с GitHub Actions

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          pip install -r requirements-dev.txt
          pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /opt/botcast
            git pull
            docker-compose up -d --build
```

## 📊 Мониторинг

### Логирование

Настройка логирования в `app/core/logging.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger("botcast")
    logger.setLevel(logging.INFO)
    
    # Файловый хендлер с ротацией
    file_handler = RotatingFileHandler(
        "logs/botcast.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    
    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    return logger
```

### Метрики

Интеграция с Prometheus:

```python
from prometheus_client import Counter, Histogram, generate_latest

# Метрики
request_count = Counter(
    'botcast_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'botcast_request_duration_seconds',
    'Request duration',
    ['method', 'endpoint']
)

@app.get("/metrics")
async def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )
```

### Healthcheck

```python
@app.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    # Проверка БД
    try:
        await db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Проверка Redis
    try:
        await redis.ping()
        redis_status = "healthy"
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "healthy" and redis_status == "healthy" else "unhealthy",
        "services": {
            "database": db_status,
            "redis": redis_status
        }
    }
```

## 🗺 Дорожная карта

### Версия 0.1.0 (MVP) ✅
- [x] Базовая структура проекта
- [x] Аутентификация пользователей
- [x] CRUD операции для ботов
- [x] Интеграция с PostgreSQL
- [x] Systemd службы
- [x] Webhook интеграция
- [x] Система рассылок с ARQ

### Версия 0.2.0 (Q1 2025) 🚧
- [ ] Полноценная веб-панель на React
- [ ] Шаблоны сообщений
- [ ] Импорт подписчиков из CSV/Excel
- [ ] Расширенная аналитика

### Версия 0.3.0 (Q2 2025) 📋
- [ ] Планировщик рассылок (cron)
- [ ] Сегментация аудитории
- [ ] A/B тестирование
- [ ] Экспорт статистики в PDF/Excel

### Версия 0.4.0 (Q3 2025) 📋
- [ ] Многоязычность интерфейса
- [ ] Интеграция с CRM системами
- [ ] API для внешних разработчиков
- [ ] Плагины и расширения

### Версия 1.0.0 (Q4 2025) 🎯
- [ ] Полноценная SaaS платформа
- [ ] Биллинг и подписки
- [ ] Мобильное приложение
- [ ] Enterprise функции

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие BotCast! Вот как вы можете помочь:

### Процесс внесения изменений

1. **Fork репозитория**
   ```bash
   # Нажмите кнопку Fork на GitHub
   git clone https://github.com/YOUR_USERNAME/botcast.git
   cd botcast
   ```

2. **Создайте ветку для изменений**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Внесите изменения**
   - Следуйте стилю кода проекта
   - Добавьте тесты для новой функциональности
   - Обновите документацию

4. **Проверьте код**
   ```bash
   make lint
   make test
   ```

5. **Создайте commit**
   ```bash
   git commit -m "feat: добавлена потрясающая функция"
   ```

6. **Отправьте изменения**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Создайте Pull Request**
   - Опишите изменения
   - Укажите связанные issues
   - Дождитесь review

### Соглашения о коммитах

Используем [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - новая функциональность
- `fix:` - исправление бага
- `docs:` - изменения документации
- `style:` - форматирование кода
- `refactor:` - рефакторинг
- `test:` - добавление тестов
- `chore:` - обновление зависимостей

### Сообщения об ошибках

При создании issue указывайте:
1. Версию BotCast
2. Шаги для воспроизведения
3. Ожидаемое поведение
4. Фактическое поведение
5. Логи (если есть)

### Предложения улучшений

Создайте issue с тегом `enhancement` и опишите:
- Проблему, которую решает предложение
- Предлагаемое решение
- Альтернативные варианты

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

```
MIT License

Copyright (c) 2024 BotCast

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🔒 Безопасность

### Ответственное раскрытие

Если вы обнаружили уязвимость:

1. **НЕ** создавайте публичный issue
2. Отправьте описание на security@botcast.ru
3. Включите:
   - Описание уязвимости
   - Шаги воспроизведения
   - Возможные последствия
   - Предложения по исправлению

Мы ответим в течение 48 часов.

### Лучшие практики безопасности

- Всегда используйте HTTPS в production
- Регулярно обновляйте зависимости
- Используйте сильные пароли и 2FA
- Ограничивайте доступ к API rate limiting
- Логируйте подозрительную активность
- Шифруйте чувствительные данные

## 💰 Спонсорство

Если BotCast помог вашему бизнесу, рассмотрите возможность спонсорства:

- **GitHub Sponsors**: [Sponsor on GitHub](https://github.com/sponsors/wobujidao)
- **Patreon**: [Support on Patreon](https://patreon.com/botcast)
- **Криптовалюта**:
  - BTC: `bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh`
  - ETH: `0x71C7bb8b2947cF0A6f8b4A6f1F9f5b5F8F8f8f8f8`

Спонсоры получают:
- Приоритетную поддержку
- Ранний доступ к новым функциям
- Упоминание в README
- Эксклюзивные обновления

## 📞 Контакты

- **Email**: support@botcast.ru
- **Telegram**: [@botcast_support](https://t.me/botcast_support)
- **Discord**: [BotCast Community](https://discord.gg/botcast)
- **Twitter**: [@botcast_io](https://twitter.com/botcast_io)

### Команда

- **wobujidao** - Основатель и главный разработчик
  - GitHub: [@wobujidao](https://github.com/wobujidao)
  - Email: wobujidao@botcast.ru

### Сообщество

- [Telegram чат](https://t.me/botcast_chat) - Общение с сообществом
- [Stack Overflow](https://stackoverflow.com/questions/tagged/botcast) - Вопросы и ответы
- [YouTube](https://youtube.com/@botcast) - Видео туториалы
- [Blog](https://blog.botcast.ru) - Новости и статьи

## 🙏 Благодарности

Спасибо всем, кто помог в создании BotCast:

- [FastAPI](https://fastapi.tiangolo.com/) - За отличный веб-фреймворк
- [SQLAlchemy](https://www.sqlalchemy.org/) - За мощный ORM
- [Aiogram](https://aiogram.dev/) - За удобную работу с Telegram API
- Всем контрибьюторам и пользователям проекта

---

<div align="center">
  <p>
    Сделано с ❤️ командой BotCast
  </p>
  <p>
    <a href="https://botcast.ru">botcast.ru</a> •
    <a href="https://docs.botcast.ru">Документация</a> •
    <a href="https://api.botcast.ru">API</a>
  </p>
</div>
