from pydantic import BaseModel
from typing import Literal

class PointOfInterest(BaseModel):
    """A model for a point of interest like a campground or a toilet."""
    name: str
    type: Literal['campground', 'toilet']
    latitude: float
    longitude: float
    address: str
