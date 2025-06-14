from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth_router, bots_router, broadcasts_router, webhook_router, users_router

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",  # Альтернативный порт Vite
        "http://192.168.5.9:5173",  # Frontend production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth_router)
app.include_router(bots_router)
app.include_router(broadcasts_router)
app.include_router(webhook_router)
app.include_router(users_router)

@app.get("/")
async def root():
    return {"message": "Welcome to BotCast API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
