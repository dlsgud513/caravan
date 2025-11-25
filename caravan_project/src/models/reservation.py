from pydantic import BaseModel, validator
from datetime import date
from typing import Optional

class ReservationCreate(BaseModel):
    """A model for creating a new reservation, with data from the user."""
    caravan_id: int
    start_date: date
    end_date: date

class Reservation(BaseModel):
    """Full Reservation model."""
    reservation_id: Optional[int] = None
    user_id: int
    caravan_id: int
    start_date: date
    end_date: date
    total_price: float
    status: str = 'pending' # e.g., pending, confirmed, cancelled

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v