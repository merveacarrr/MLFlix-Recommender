from datetime import timedelta
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import create_access_token, get_current_user
from app.db.session import get_db
from app.schemas.user import User, UserCreate, Token, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.models.recommender import MovieRecommender

router = APIRouter()
user_service = UserService()
recommender = MovieRecommender()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    user_service = UserService()
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=User)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    user_service = UserService()
    user = user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = user_service.create_user(db, user_in.email, user_in.password)
    return user

@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return user_service.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_user = user_service.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, 
    user: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    updated_user = user_service.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return updated_user

@router.delete("/{user_id}")
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    success = user_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return {"message": "Kullanıcı başarıyla silindi"}

@router.get("/{user_id}/recommendations", response_model=List[dict])
def get_user_recommendations(
    user_id: int, 
    n_recommendations: int = 5, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Öneri sistemini güncelle
    ratings = user_service.get_all_ratings(db)
    recommender.update_recommendations(ratings)
    
    # Kullanıcı için önerileri al
    recommended_movie_ids = recommender.get_movie_recommendations(user_id, n_recommendations)
    recommended_movies = [user_service.get_movie_details(db, mid) for mid in recommended_movie_ids]
    return [movie for movie in recommended_movies if movie is not None]

@router.get("/{user_id}/stats")
def get_user_stats(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return user_service.get_user_statistics(db, user_id) 