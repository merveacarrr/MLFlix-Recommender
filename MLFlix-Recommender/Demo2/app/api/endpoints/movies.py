from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.movie import MovieCreate, MovieResponse, MovieUpdate
from app.services.movie_service import MovieService
from app.models.recommender import MovieRecommender

router = APIRouter()
movie_service = MovieService()
recommender = MovieRecommender()

@router.post("/", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    return movie_service.create_movie(db, movie)

@router.get("/", response_model=List[MovieResponse])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return movie_service.get_movies(db, skip=skip, limit=limit)

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = movie_service.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Film bulunamadı")
    return movie

@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    updated_movie = movie_service.update_movie(db, movie_id, movie)
    if not updated_movie:
        raise HTTPException(status_code=404, detail="Film bulunamadı")
    return updated_movie

@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    success = movie_service.delete_movie(db, movie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Film bulunamadı")
    return {"message": "Film başarıyla silindi"}

@router.get("/{movie_id}/similar", response_model=List[MovieResponse])
def get_similar_movies(movie_id: int, n_similar: int = 5, db: Session = Depends(get_db)):
    # Öneri sistemini güncelle
    ratings = movie_service.get_all_ratings(db)
    recommender.update_recommendations(ratings)
    
    # Benzer filmleri bul
    similar_movie_ids = recommender.get_similar_movies(movie_id, n_similar)
    similar_movies = [movie_service.get_movie(db, mid) for mid in similar_movie_ids]
    return [movie for movie in similar_movies if movie is not None]

@router.get("/trending", response_model=List[MovieResponse])
def get_trending_movies(db: Session = Depends(get_db)):
    return movie_service.get_trending_movies(db)

@router.get("/genre/{genre}", response_model=List[MovieResponse])
def get_movies_by_genre(genre: str, db: Session = Depends(get_db)):
    return movie_service.get_movies_by_genre(db, genre)

@router.get("/")
def read_movies(db: Session = Depends(get_db)):
    return {"message": "Movies endpoint"} 