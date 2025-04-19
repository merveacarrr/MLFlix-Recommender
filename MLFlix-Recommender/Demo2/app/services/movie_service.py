from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Movie, Rating
from app.schemas.movie import MovieCreate, MovieUpdate

class MovieService:
    def create_movie(self, db: Session, movie: MovieCreate) -> Movie:
        db_movie = Movie(**movie.model_dump())
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie

    def get_movies(self, db: Session, skip: int = 0, limit: int = 100) -> List[Movie]:
        return db.query(Movie).offset(skip).limit(limit).all()

    def get_movie(self, db: Session, movie_id: int) -> Optional[Movie]:
        return db.query(Movie).filter(Movie.id == movie_id).first()

    def update_movie(self, db: Session, movie_id: int, movie: MovieUpdate) -> Optional[Movie]:
        db_movie = self.get_movie(db, movie_id)
        if not db_movie:
            return None
        
        update_data = movie.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_movie, field, value)
        
        db.commit()
        db.refresh(db_movie)
        return db_movie

    def delete_movie(self, db: Session, movie_id: int) -> bool:
        db_movie = self.get_movie(db, movie_id)
        if not db_movie:
            return False
        
        db.delete(db_movie)
        db.commit()
        return True

    def get_all_ratings(self, db: Session) -> List[dict]:
        ratings = db.query(Rating).all()
        return [
            {
                "user_id": rating.user_id,
                "movie_id": rating.movie_id,
                "rating": rating.rating
            }
            for rating in ratings
        ]

    def get_trending_movies(self, db: Session, limit: int = 10) -> List[Movie]:
        return (
            db.query(Movie)
            .order_by(Movie.average_rating.desc())
            .limit(limit)
            .all()
        )

    def get_movies_by_genre(self, db: Session, genre: str) -> List[Movie]:
        return db.query(Movie).filter(Movie.genre == genre).all() 