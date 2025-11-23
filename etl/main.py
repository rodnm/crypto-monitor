import requests
import pandas as pd
import os
from datetime import datetime

# Configuration
API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": "true"
}
DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "crypto_market.csv")

def extract_data():
    """Fetches data from CoinGecko API."""
    try:
        print(f"Fetching data from {API_URL}...")
        response = requests.get(API_URL, params=PARAMS, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"Successfully fetched {len(data)} records.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def transform_data(data):
    """Cleans and structures the data."""
    if not data:
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    
    # Select relevant columns
    cols_to_keep = [
        'id', 'symbol', 'name', 'current_price', 'market_cap', 
        'total_volume', 'price_change_percentage_24h', 'sparkline_in_7d'
    ]
    df = df[cols_to_keep]
    
    # Rename columns for clarity
    df.columns = [
        'ID', 'Symbol', 'Name', 'Price (USD)', 'Market Cap', 
        'Volume (24h)', 'Change (24h) %', 'Sparkline (7d)'
    ]
    
    # Extract prices from sparkline dictionary
    df['Sparkline (7d)'] = df['Sparkline (7d)'].apply(lambda x: x.get('price') if isinstance(x, dict) else [])

    # Add timestamp
    df['Last Updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Uppercase Symbol
    df['Symbol'] = df['Symbol'].str.upper()
    
    return df

def load_data(df):
    """Saves data to CSV."""
    if df.empty:
        print("No data to save.")
        return
    
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Data saved to {OUTPUT_FILE}")

def run_etl():
    """Main ETL function."""
    print("Starting ETL process...")
    raw_data = extract_data()
    clean_df = transform_data(raw_data)
    load_data(clean_df)
    print("ETL process completed.")

if __name__ == "__main__":
    run_etl()
