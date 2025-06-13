#!/usr/bin/env python3
"""
Скрипт для настройки webhook для Telegram бота
"""
import asyncio
import httpx
import sys

TELEGRAM_API = "https://api.telegram.org/bot{token}"
WEBHOOK_URL = "https://your-domain.com/telegram/webhook/{token}"  # Замените на ваш домен

async def setup_webhook(bot_token: str, webhook_url: str = None):
    if not webhook_url:
        webhook_url = WEBHOOK_URL.format(token=bot_token)
    
    async with httpx.AsyncClient() as client:
        # Получаем информацию о боте
        response = await client.get(f"{TELEGRAM_API.format(token=bot_token)}/getMe")
        if response.status_code != 200:
            print(f"❌ Ошибка: неверный токен бота")
            return
        
        bot_info = response.json()["result"]
        print(f"🤖 Бот: @{bot_info['username']} ({bot_info['first_name']})")
        
        # Устанавливаем webhook
        response = await client.post(
            f"{TELEGRAM_API.format(token=bot_token)}/setWebhook",
            json={"url": webhook_url}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result["ok"]:
                print(f"✅ Webhook установлен: {webhook_url}")
            else:
                print(f"❌ Ошибка: {result['description']}")
        else:
            print(f"❌ Ошибка HTTP: {response.status_code}")
        
        # Проверяем webhook
        response = await client.get(f"{TELEGRAM_API.format(token=bot_token)}/getWebhookInfo")
        webhook_info = response.json()["result"]
        print(f"\n📋 Информация о webhook:")
        print(f"   URL: {webhook_info['url']}")
        print(f"   Pending updates: {webhook_info['pending_update_count']}")
        if webhook_info.get("last_error_message"):
            print(f"   ❌ Последняя ошибка: {webhook_info['last_error_message']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python setup_webhook.py <bot_token> [webhook_url]")
        print("\nДля локального тестирования используйте ngrok:")
        print("1. Установите ngrok: https://ngrok.com/download")
        print("2. Запустите: ngrok http 8000")
        print("3. Используйте URL от ngrok")
        sys.exit(1)
    
    bot_token = sys.argv[1]
    webhook_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    asyncio.run(setup_webhook(bot_token, webhook_url))
