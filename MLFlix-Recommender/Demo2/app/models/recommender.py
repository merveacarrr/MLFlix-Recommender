import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
import pandas as pd

class MovieRecommender:
    def __init__(self):
        self.user_movie_matrix = None
        self.movie_similarity = None
        self.user_similarity = None
        
    def create_user_movie_matrix(self, ratings: List[Dict[str, Any]]) -> None:
        """Kullanıcı-film matrisini oluşturur"""
        df = pd.DataFrame(ratings)
        self.user_movie_matrix = df.pivot(
            index='user_id',
            columns='movie_id',
            values='rating'
        ).fillna(0)
        
    def calculate_similarities(self) -> None:
        """Film ve kullanıcı benzerliklerini hesaplar"""
        if self.user_movie_matrix is not None:
            # Film benzerliği
            self.movie_similarity = cosine_similarity(self.user_movie_matrix.T)
            # Kullanıcı benzerliği
            self.user_similarity = cosine_similarity(self.user_movie_matrix)
            
    def get_movie_recommendations(self, user_id: int, n_recommendations: int = 5) -> List[int]:
        """Kullanıcı için film önerileri oluşturur"""
        if user_id not in self.user_movie_matrix.index:
            return []
            
        # Kullanıcının izlemediği filmleri bul
        user_ratings = self.user_movie_matrix.loc[user_id]
        unwatched_movies = user_ratings[user_ratings == 0].index
        
        if len(unwatched_movies) == 0:
            return []
            
        # Benzer kullanıcıların puanlarını kullanarak tahmin yap
        user_similarities = self.user_similarity[self.user_movie_matrix.index.get_loc(user_id)]
        weighted_ratings = np.dot(user_similarities, self.user_movie_matrix)
        
        # Önerileri sırala
        recommendations = pd.Series(weighted_ratings, index=self.user_movie_matrix.columns)
        recommendations = recommendations[unwatched_movies].sort_values(ascending=False)
        
        return recommendations.head(n_recommendations).index.tolist()
        
    def get_similar_movies(self, movie_id: int, n_similar: int = 5) -> List[int]:
        """Benzer filmleri bulur"""
        if movie_id not in self.user_movie_matrix.columns:
            return []
            
        movie_similarities = self.movie_similarity[self.user_movie_matrix.columns.get_loc(movie_id)]
        similar_movies = pd.Series(movie_similarities, index=self.user_movie_matrix.columns)
        similar_movies = similar_movies.sort_values(ascending=False)
        
        # Kendisini çıkar
        similar_movies = similar_movies[similar_movies.index != movie_id]
        
        return similar_movies.head(n_similar).index.tolist()
        
    def update_recommendations(self, new_ratings: List[Dict[str, Any]]) -> None:
        """Yeni puanlamalarla öneri sistemini günceller"""
        self.create_user_movie_matrix(new_ratings)
        self.calculate_similarities() 