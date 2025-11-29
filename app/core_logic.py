import pandas as pd
import numpy as np
import h3
from sklearn.ensemble import RandomForestRegressor
from app.data_gen import generate_mock_historical_data

class PricingEngine:
    def __init__(self):
        self.model = None
        self.is_trained = False
        
    def train_model(self):
        """
        Trains a simple regressor to predict demand based on location (H3) and time.
        In production, this would load a pre-trained model artifact.
        """
        print("Training Pricing Engine...")
        df = generate_mock_historical_data()
        
        # Feature Engineering for Model
        # We need to encode H3. For simplicity, we use lat/lon centroid of the hex.
        X = df[['lat', 'lon', 'hour_of_day']]
        y = df['demand_score']
        
        self.model = RandomForestRegressor(n_estimators=50, max_depth=10)
        self.model.fit(X, y)
        self.is_trained = True
        print("Pricing Engine Trained.")

    def calculate_surge(self, demand: float, supply: int) -> float:
        """
        Dynamic Pricing Logic (Simplified Causal approach).
        Surge = 1.0 + (Elasticity_Factor * (Demand / Supply_Ratio))
        """
        if supply == 0:
            return 3.0 # Max surge if no drivers
            
        utilization = demand / supply
        
        # Base surge logic
        if utilization < 0.8:
            return 1.0 # No surge
        elif utilization < 1.2:
            return 1.2 # Mild surge
        elif utilization < 2.0:
            return 1.8 # High surge
        else:
            return 2.5 # Super surge

    def predict_price(self, lat: float, lon: float, hour: int):
        if not self.is_trained:
            self.train_model()
            
        # 1. Spatial Indexing
        # FIX: Changed geo_to_h3 to latlng_to_cell for H3 v4.0+
        h3_index = h3.latlng_to_cell(lat, lon, 9)
        
        # 2. Predict Demand
        # We pass lat/lon back to model (simplified)
        predicted_demand = self.model.predict([[lat, lon, hour]])[0]
        
        # 3. Simulate Supply (Mock Real-time availability)
        # Random supply based on inverse of demand to simulate scarcity
        available_drivers = max(1, int(np.random.normal(20, 5) - (predicted_demand * 0.2)))
        
        # 4. Calculate Surge
        surge = self.calculate_surge(predicted_demand, available_drivers)
        
        # 5. Final Price
        base_fare = 3.50 + (np.random.random() * 2) # Random distance proxy
        final_price = round(base_fare * surge, 2)
        
        return {
            "hex_id": h3_index,
            "predicted_demand": round(predicted_demand, 2),
            "available_drivers": available_drivers,
            "surge_multiplier": surge,
            "base_price": round(base_fare, 2),
            "final_price": final_price,
            "message": "Surge Applied!" if surge > 1.0 else "Standard Pricing"
        }