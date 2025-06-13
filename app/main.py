from fastapi import FastAPI
from app.core.config import settings
from app.api import auth_router, bots_router, broadcasts_router, webhook_router

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# Подключаем роутеры
app.include_router(auth_router)
app.include_router(bots_router)
app.include_router(broadcasts_router)
app.include_router(webhook_router)

@app.get("/")
async def root():
    return {"message": "Welcome to BotCast API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
