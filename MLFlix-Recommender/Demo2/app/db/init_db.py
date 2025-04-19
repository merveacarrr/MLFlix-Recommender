from sqlalchemy import create_engine
from app.db.base_class import Base
from app.db.models import User, Movie, Rating
from app.core.config import settings

def init_db():
    # Veritabanı bağlantısını oluştur
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    # Tabloları oluştur
    Base.metadata.create_all(bind=engine)
    
    print("Veritabanı tabloları başarıyla oluşturuldu!")

if __name__ == "__main__":
    init_db() 