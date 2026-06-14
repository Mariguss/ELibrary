from fastapi import APIRouter
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.role import router as role_router
from app.api.v1.endpoints.book import router as book_router
from app.api.v1.endpoints.genre import router as genre_router

routers = APIRouter()

routers.include_router(auth_router)
routers.include_router(user_router)
routers.include_router(role_router)
routers.include_router(book_router)
routers.include_router(genre_router)
