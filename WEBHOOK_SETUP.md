# Настройка Webhook для BotCast

## Локальное тестирование с ngrok

1. Установите ngrok: https://ngrok.com/download
2. Запустите туннель:
   ```bash
   ngrok http 8000
   ```
3. Скопируйте HTTPS URL (например: https://abc123.ngrok.io)
4. Настройте webhook:
   ```bash
   python setup_webhook.py YOUR_BOT_TOKEN https://abc123.ngrok.io/telegram/webhook/YOUR_BOT_TOKEN
   ```

## Продакшн настройка

1. Убедитесь, что у вас есть SSL сертификат (Telegram требует HTTPS)
2. Настройте nginx для проксирования на порт 8000
3. Запустите:
   ```bash
   python setup_webhook.py YOUR_BOT_TOKEN https://yourdomain.com/telegram/webhook/YOUR_BOT_TOKEN
   ```

## Проверка webhook

```bash
# Проверить статус webhook
curl https://api.telegram.org/botYOUR_BOT_TOKEN/getWebhookInfo

# Тест локально
python test_webhook.py
```

## Как это работает

1. Пользователь отправляет /start боту
2. Telegram отправляет webhook на наш endpoint
3. Система автоматически регистрирует подписчика
4. Бот отправляет приветственное сообщение
