import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.base_class import Base
from app.db.models import User, Movie, Rating
from app.db.session import engine

def init_db():
    # Önce tabloları sil
    Base.metadata.drop_all(bind=engine)
    # Sonra yeniden oluştur
    Base.metadata.create_all(bind=engine)
    print("Veritabanı şeması oluşturuldu!")

if __name__ == "__main__":
    init_db() 