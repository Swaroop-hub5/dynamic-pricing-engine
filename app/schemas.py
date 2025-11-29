from pydantic import BaseModel
from typing import Optional

class RideRequest(BaseModel):
    lat: float
    lon: float
    timestamp: Optional[str] = None

class PricingResponse(BaseModel):
    hex_id: str
    predicted_demand: float
    available_drivers: int
    surge_multiplier: float
    base_price: float
    final_price: float
    message: str