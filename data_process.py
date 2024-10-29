import pandas as pd
from datetime import datetime, time
from get_data import fetch_data_from_api

# Global variable to store the data
data_store = pd.DataFrame()

def process_data(data):
    if data is None:
        print("No data received from API")
        return pd.DataFrame()  
    try:
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            print(f"Unexpected data format. Expected list or dict, got {type(data)}")
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        if df.empty:
            print("DataFrame is empty after conversion")
            return df

        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%b-%Y %H:%M:%S', errors='coerce')
        
        required_columns = ['timestamp', 'pH', 'TDS', 'Depth', 'FlowInd']
        for col in required_columns:
            if col not in df.columns:
                print(f"Missing column: {col}")
                df[col] = None
        
        return df.sort_values('timestamp')
    except Exception as e:
        print(f"Error processing data: {e}")
        return pd.DataFrame()

def process_and_store_data(api_url):
    global data_store
    data = fetch_data_from_api(api_url)
    if data:
        new_data = process_data(data)
        data_store = pd.concat([data_store, new_data]).drop_duplicates().sort_values('timestamp')
        print("Data updated successfully")
    else:
        print("No new data to update")
    
def get_todays_data():
    global data_store
    today = datetime.now().date()
    try:
        if not pd.api.types.is_datetime64_any_dtype(data_store['timestamp']):
            data_store['timestamp'] = pd.to_datetime(data_store['timestamp'])
        return data_store[data_store['timestamp'].dt.date == today]
    except Exception as e:
        print("Error occurred in get_todays_data:", e)
        return pd.DataFrame()

def get_historical_data(start_date, end_date):
    global data_store
    try:
        if not pd.api.types.is_datetime64_any_dtype(data_store['timestamp']):
            data_store['timestamp'] = pd.to_datetime(data_store['timestamp'])
            
        # Convert dates to datetime if they're not already
        start_date = pd.to_datetime(start_date).date()
        end_date = pd.to_datetime(end_date).date()
        
        # Filter data for the date range
        mask = (data_store['timestamp'].dt.date >= start_date) & (data_store['timestamp'].dt.date <= end_date)
        return data_store[mask].copy()
    except Exception as e:
        print("Error occurred in get_historical_data:", e)
        return pd.DataFrame()