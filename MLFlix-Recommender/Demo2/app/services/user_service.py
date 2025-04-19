from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.db.models import User, Rating, Movie
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.models.user import User as UserModel

class UserService:
    def __init__(self):
        pass

    def create_user(self, db: Session, email: str, password: str) -> UserModel:
        hashed_password = get_password_hash(password)
        user = UserModel(email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[UserModel]:
        return db.query(UserModel).offset(skip).limit(limit).all()

    def get_user(self, db: Session, user_id: int) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.email == email).first()

    def update_user(self, db: Session, user_id: int, user: UserUpdate) -> Optional[UserModel]:
        db_user = self.get_user(db, user_id)
        if not db_user:
            return None
        
        update_data = user.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(self, db: Session, user_id: int) -> bool:
        db_user = self.get_user(db, user_id)
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True

    def authenticate(self, db: Session, email: str, password: str) -> Optional[UserModel]:
        user = self.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

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

    def get_movie_details(self, db: Session, movie_id: int) -> Optional[Dict[str, Any]]:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            return None
        return {
            "id": movie.id,
            "title": movie.title,
            "genre": movie.genre,
            "director": movie.director,
            "average_rating": movie.average_rating
        }

    def get_user_statistics(self, db: Session, user_id: int) -> Dict[str, Any]:
        user = self.get_user(db, user_id)
        if not user:
            return {}
        
        ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
        watched_movies = len(user.watched_movies)
        average_rating = sum(r.rating for r in ratings) / len(ratings) if ratings else 0
        
        return {
            "total_ratings": len(ratings),
            "watched_movies": watched_movies,
            "average_rating": round(average_rating, 2),
            "favorite_genre": self._get_favorite_genre(db, user_id)
        }

    def _get_favorite_genre(self, db: Session, user_id: int) -> str:
        movies = db.query(Movie).join(Rating).filter(Rating.user_id == user_id).all()
        if not movies:
            return "Henüz film izlenmemiş"
        
        genre_counts = {}
        for movie in movies:
            genre_counts[movie.genre] = genre_counts.get(movie.genre, 0) + 1
        
        return max(genre_counts.items(), key=lambda x: x[1])[0]

    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[UserModel]:
        user = self.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user 