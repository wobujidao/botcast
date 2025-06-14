from fastapi import APIRouter, Depends
from app.models.user import User
from app.schemas.user import UserResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Получить информацию о текущем пользователе"""
    return current_user
