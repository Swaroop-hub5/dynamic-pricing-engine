from fastapi import FastAPI
from app.schemas import RideRequest, PricingResponse
from app.core_logic import PricingEngine
from datetime import datetime

app = FastAPI(title="Bolt-style Dynamic Pricing Engine")

# Initialize and train model on startup
engine = PricingEngine()
engine.train_model()

@app.get("/")
def health_check():
    return {"status": "active", "service": "pricing-engine-v1"}

@app.post("/predict_fare", response_model=PricingResponse)
def predict_fare(request: RideRequest):
    """
    Accepts GPS coordinates, converts to H3, predicts demand, and returns dynamic price.
    """
    current_hour = datetime.now().hour
    
    result = engine.predict_price(
        lat=request.lat,
        lon=request.lon,
        hour=current_hour
    )
    
    return result

@app.get("/heat_map_data")
def get_heat_map_data():
    """
    Returns data to visualize the demand layer on the frontend map.
    """
    # Generate fresh random data for visualization
    from app.data_gen import generate_mock_historical_data
    df = generate_mock_historical_data(n_samples=200)
    return df[['lat', 'lon', 'demand_score', 'base_price']].to_dict(orient='records')