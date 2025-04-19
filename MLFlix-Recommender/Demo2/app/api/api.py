from fastapi import APIRouter
from app.api.endpoints import users, movies

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(movies.router, prefix="/movies", tags=["movies"]) 