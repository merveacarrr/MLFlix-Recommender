import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from app.db.models import User, Movie, Rating
from app.db.session import SessionLocal
import random
from datetime import datetime, timedelta

# Örnek veriler
genres = ["Aksiyon", "Macera", "Animasyon", "Komedi", "Suç", "Belgesel", 
          "Drama", "Aile", "Fantastik", "Tarih", "Korku", "Müzik", 
          "Gizem", "Romantik", "Bilim Kurgu", "TV Film", "Gerilim", "Savaş", "Western"]

directors = ["Christopher Nolan", "Quentin Tarantino", "Martin Scorsese", 
             "Steven Spielberg", "James Cameron", "Ridley Scott", 
             "David Fincher", "Wes Anderson", "Alfred Hitchcock"]

def generate_movies(n=100):
    movies = []
    for i in range(n):
        movie = {
            "title": f"Film {i+1}",
            "release_year": random.randint(1990, 2023),
            "genre": random.choice(genres),
            "director": random.choice(directors),
            "description": f"Bu film {random.choice(genres)} türünde bir başyapıttır.",
            "average_rating": round(random.uniform(1, 10), 1)
        }
        movies.append(movie)
    return movies

def generate_users(n=50):
    users = []
    for i in range(n):
        user = {
            "username": f"user{i+1}",
            "email": f"user{i+1}@example.com",
            "hashed_password": f"hashed_password_{i+1}"
        }
        users.append(user)
    return users

def generate_ratings(users, movies, n_ratings_per_user=20):
    ratings = []
    for user in users:
        # Her kullanıcı için rastgele filmler seç
        user_movies = random.sample(movies, min(n_ratings_per_user, len(movies)))
        for movie in user_movies:
            rating = {
                "user_id": user.id,
                "movie_id": movie.id,
                "rating": round(random.uniform(1, 10), 1),
                "created_at": datetime.now() - timedelta(days=random.randint(0, 365))
            }
            ratings.append(rating)
    return ratings

def save_to_csv(movies, users, ratings):
    # CSV dosyaları için klasör oluştur
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir = os.path.join(current_dir, 'csv')
    os.makedirs(csv_dir, exist_ok=True)
    
    # Verileri DataFrame'lere dönüştür
    movies_df = pd.DataFrame(movies)
    users_df = pd.DataFrame(users)
    ratings_df = pd.DataFrame(ratings)
    
    # CSV dosyalarını kaydet
    movies_df.to_csv(os.path.join(csv_dir, 'movies.csv'), index=False)
    users_df.to_csv(os.path.join(csv_dir, 'users.csv'), index=False)
    ratings_df.to_csv(os.path.join(csv_dir, 'ratings.csv'), index=False)
    
    print("Veriler CSV dosyalarına kaydedildi!")

def main():
    db = SessionLocal()
    
    try:
        # Filmleri oluştur
        movies = generate_movies()
        movie_objects = []
        for movie_data in movies:
            movie = Movie(**movie_data)
            db.add(movie)
            movie_objects.append(movie)
        db.commit()
        
        # Kullanıcıları oluştur
        users = generate_users()
        user_objects = []
        for user_data in users:
            user = User(**user_data)
            db.add(user)
            user_objects.append(user)
        db.commit()
        
        # Puanlamaları oluştur
        ratings = generate_ratings(user_objects, movie_objects)
        rating_objects = []
        for rating_data in ratings:
            rating = Rating(**rating_data)
            db.add(rating)
            rating_objects.append(rating_data)
        db.commit()
        
        # Verileri CSV olarak kaydet
        save_to_csv(movies, users, rating_objects)
        
        print("Örnek veriler başarıyla oluşturuldu ve CSV'lere kaydedildi!")
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 