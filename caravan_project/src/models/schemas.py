from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class ReservationDetails(BaseModel):
    """Schema for returning reservation details including caravan info."""
    reservation_id: int
    start_date: date
    end_date: date
    total_price: float
    status: str
    caravan_name: str
    caravan_image_url: Optional[str] = None
