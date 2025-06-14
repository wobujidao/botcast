#!/usr/bin/env python3
"""
Скрипт для добавления тестового бота
"""
import asyncio
import httpx
import sys

API_URL = "http://localhost:8000"

async def add_bot(email: str, password: str, bot_token: str, bot_name: str = None):
    async with httpx.AsyncClient() as client:
        # Авторизация
        print("🔐 Авторизация...")
        login_data = {"email": email, "password": password}
        response = await client.post(f"{API_URL}/auth/login", json=login_data)
        
        if response.status_code != 200:
            print(f"❌ Ошибка авторизации: {response.text}")
            return
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Добавление бота
        print("🤖 Добавление бота...")
        bot_data = {
            "bot_token": bot_token,
            "bot_name": bot_name
        }
        
        response = await client.post(
            f"{API_URL}/bots", 
            json=bot_data, 
            headers=headers,
            follow_redirects=True
        )
        
        if response.status_code == 200:
            bot = response.json()
            print(f"✅ Бот успешно добавлен!")
            print(f"   ID: {bot['id']}")
            print(f"   Username: @{bot['bot_username']}")
            print(f"   Name: {bot['bot_name']}")
        else:
            print(f"❌ Ошибка: {response.json()['detail']}")

if __name__ == "__main__":
    print("Использование:")
    print("  python add_test_bot.py <email> <password> <bot_token> [bot_name]")
    print("\nПример:")
    print("  python add_test_bot.py user@example.com password123 123456:ABC-DEF... 'My Bot'")
    
    if len(sys.argv) < 4:
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    bot_token = sys.argv[3]
    bot_name = sys.argv[4] if len(sys.argv) > 4 else None
    
    asyncio.run(add_bot(email, password, bot_token, bot_name))
