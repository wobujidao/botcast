#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API BotCast
"""
import asyncio
import httpx
import json
from datetime import datetime

API_URL = "http://localhost:8000"

async def test_api():
    async with httpx.AsyncClient() as client:
        print("🔍 Тестирование BotCast API\n")
        
        # 1. Проверка здоровья
        print("1️⃣ Проверка здоровья API...")
        response = await client.get(f"{API_URL}/health")
        print(f"   Статус: {response.status_code}")
        print(f"   Ответ: {response.json()}\n")
        
        # 2. Регистрация пользователя
        print("2️⃣ Регистрация пользователя...")
        test_email = f"test_{datetime.now().timestamp()}@example.com"
        register_data = {
            "email": test_email,
            "password": "TestPassword123!"
        }
        response = await client.post(f"{API_URL}/auth/register", json=register_data)
        if response.status_code == 200:
            user = response.json()
            print(f"   ✅ Пользователь создан: {user['email']}")
        else:
            print(f"   ❌ Ошибка: {response.text}")
        
        # 3. Авторизация
        print("\n3️⃣ Авторизация...")
        login_data = {
            "email": test_email,
            "password": "TestPassword123!"
        }
        response = await client.post(f"{API_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print(f"   ✅ Токен получен: {token[:20]}...")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            return
        
        # Заголовки с токеном
        headers = {"Authorization": f"Bearer {token}"}
        
        # 4. Получение списка ботов
        print("\n4️⃣ Получение списка ботов...")
        response = await client.get(f"{API_URL}/bots", headers=headers, follow_redirects=True)
        print(f"   Статус: {response.status_code}")
        if response.status_code == 200:
            bots = response.json()
            print(f"   Ботов найдено: {len(bots)}")
        else:
            print(f"   Ответ: {response.text}")
        
        # 5. Попытка добавить бота (без реального токена)
        print("\n5️⃣ Попытка добавить бота...")
        bot_data = {
            "bot_token": "test_token_123456:ABC-DEF",
            "bot_name": "Test Bot"
        }
        response = await client.post(f"{API_URL}/bots", json=bot_data, headers=headers, follow_redirects=True)
        print(f"   Статус: {response.status_code}")
        if response.status_code != 200:
            try:
                error_detail = response.json()['detail']
                print(f"   ℹ️  Ожидаемая ошибка (нужен реальный токен): {error_detail}")
            except:
                print(f"   ℹ️  Ответ: {response.text}")
        
        # 6. Получение списка рассылок
        print("\n6️⃣ Получение списка рассылок...")
        response = await client.get(f"{API_URL}/broadcasts", headers=headers, follow_redirects=True)
        print(f"   Статус: {response.status_code}")
        if response.status_code == 200:
            broadcasts = response.json()
            print(f"   Рассылок найдено: {len(broadcasts)}")
        else:
            print(f"   Ответ: {response.text}")
        
        print("\n✅ Тестирование завершено!")

if __name__ == "__main__":
    asyncio.run(test_api())
