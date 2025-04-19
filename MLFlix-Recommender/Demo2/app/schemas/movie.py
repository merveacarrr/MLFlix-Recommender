from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    release_year: int = Field(..., ge=1900, le=datetime.now().year)
    genre: str = Field(..., min_length=1, max_length=50)
    director: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    average_rating: float = Field(0.0, ge=0.0, le=10.0)

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    release_year: Optional[int] = Field(None, ge=1900, le=datetime.now().year)
    genre: Optional[str] = Field(None, min_length=1, max_length=50)
    director: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    average_rating: Optional[float] = Field(None, ge=0.0, le=10.0)

class MovieResponse(MovieBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 