"""
Generate test dataset with ~10,000 rows for MLOps pipeline testing.
This script creates realistic Bitcoin price data with randomness.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_test_data(num_rows=10000, output_file="data.csv"):
    """
    Generate realistic Bitcoin price data for testing.
    
    Args:
        num_rows: Number of rows to generate (~10,000 recommended)
        output_file: Output CSV filename
    """
    np.random.seed(42)  # For reproducibility
    
    # Start date
    start_date = datetime(2024, 1, 1, 0, 0, 0)
    
    # Initialize price at a realistic Bitcoin level
    base_price = 45000.0
    
    data = []
    price = base_price
    
    for i in range(num_rows):
        # Generate timestamp (1-minute intervals)
        timestamp = start_date + timedelta(minutes=i)
        
        # Random walk for price (±0.5% per minute)
        price_change = np.random.normal(0, 0.002) * price
        price = max(price + price_change, base_price * 0.8)  # Prevent negative
        
        # OHLCV data
        open_price = price
        high_price = price * np.random.uniform(1.0, 1.01)
        low_price = price * np.random.uniform(0.99, 1.0)
        close_price = np.random.uniform(low_price, high_price)
        volume_btc = np.random.uniform(0.1, 100.0)
        volume_usd = volume_btc * close_price
        
        data.append({
            'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume_btc': round(volume_btc, 6),
            'volume_usd': round(volume_usd, 2)
        })
    
    # Create DataFrame and save
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    
    print(f"✓ Test dataset generated: {output_file}")
    print(f"  - Total rows: {len(df)}")
    print(f"  - Date range: {df['timestamp'].iloc[0]} to {df['timestamp'].iloc[-1]}")
    print(f"  - Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
    print(f"  - File size: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")

if __name__ == "__main__":
    generate_test_data(num_rows=10000, output_file="data.csv")
