from pydantic import BaseModel, Field
from typing import Optional, List

class CaravanCreate(BaseModel):
    """Model for creating a new caravan. Fields provided by the user."""
    name: str
    type: str  # e.g., 'Motorhome', 'Campervan'
    price_per_day: float = Field(..., gt=0, description="Price must be positive")
    location: str
    sleeps: int = Field(..., gt=0)
    description: str
    image_url: Optional[str] = None

class Caravan(CaravanCreate):
    """Full Caravan model including server-set fields."""
    caravan_id: Optional[int] = None
    owner_id: int
    is_available: bool = True
    average_rating: float = 0.0
    review_count: int = 0

    class Config:
        from_attributes = True

    def update_rating(self, new_rating: int):
        """Updates the average rating and review count when a new review is added."""
        total_rating = self.average_rating * self.review_count
        self.review_count += 1
        self.average_rating = (total_rating + new_rating) / self.review_count