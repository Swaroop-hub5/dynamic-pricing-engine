import pandas as pd
import numpy as np
import h3

# Center of Tallinn, Estonia (Bolt HQ)
TALLINN_CENTER = (59.4370, 24.7536)

def generate_mock_historical_data(n_samples=5000):
    """
    Generates synthetic ride data clustered around Tallinn.
    """
    # Generate random points around Tallinn with some variance
    lats = np.random.normal(TALLINN_CENTER[0], 0.02, n_samples)
    lons = np.random.normal(TALLINN_CENTER[1], 0.04, n_samples)
    
    # Generate mock features
    # 0 = Low demand (midnight), 1 = High demand (rush hour)
    hours = np.random.randint(0, 24, n_samples)
    
    # Base Price calculation (mock)
    base_prices = np.random.uniform(3.0, 15.0, n_samples)
    
    df = pd.DataFrame({
        'lat': lats,
        'lon': lons,
        'hour_of_day': hours,
        'base_price': base_prices
    })
    
    # Convert lat/lon to H3 Index (Resolution 9 is standard for urban analysis)
    # FIX: Changed geo_to_h3 to latlng_to_cell for H3 v4.0+
    df['h3_index'] = df.apply(lambda x: h3.latlng_to_cell(x['lat'], x['lon'], 9), axis=1)
    
    # Simulate Demand: Higher demand in center and during rush hours (8-9am, 5-7pm)
    df['demand_score'] = (
        np.exp(-((df['lat'] - TALLINN_CENTER[0])**2 + (df['lon'] - TALLINN_CENTER[1])**2) * 100) * 50 + 
        np.where((df['hour_of_day'] >= 8) & (df['hour_of_day'] <= 9), 30, 0) + 
        np.where((df['hour_of_day'] >= 17) & (df['hour_of_day'] <= 19), 40, 0) + 
        np.random.normal(0, 5, n_samples) 
    )
    df['demand_score'] = df['demand_score'].clip(lower=0)
    
    return df