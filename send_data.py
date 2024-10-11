import os
import time
import pandas as pd
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

WATCH_DIR = os.getenv("WATCH_DIR")
STRAPI_URL = os.getenv("STRAPI_URL")
TOKEN = os.getenv("TOKEN")
EVENT_TYPE_MAPPING = os.getenv("EVENT_TYPE_MAPPING")

event_type_mapping = dict(item.split(":") for item in EVENT_TYPE_MAPPING.split(","))
event_type_mapping = {k: int(v) for k, v in event_type_mapping.items()}

def read_csv(file_path):
    print(f"Reading CSV file: {file_path}")
    try:
        df = pd.read_csv(file_path, delimiter=';')
        data = []
        for index, row in df.iterrows():
            # Convert date from DD.MM.YYYY to YYYY-MM-DD if it exists and is a string
            date_str = row.get("date", "")
            if pd.notna(date_str) and isinstance(date_str, str):
                try:
                    date_obj = datetime.strptime(date_str, "%d.%m.%Y")
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    formatted_date = "" 
            else:
                formatted_date = "" 


            article = {
                "title": row.get("title", ""),
                "description": row.get("description", "") if pd.notna(row.get("description")) else "",
                "slug": row.get("slug", ""),
                "event_type": int(row.get("event_type", 0)) if pd.notna(row.get("event_type")) else 0,
                "metaTitle": row.get("metaTitle", "") if pd.notna(row.get("metaTitle")) else "",
                "metaDescription": row.get("metaDescription", "") if pd.notna(row.get("metaDescription")) else "",
                "metaKeywords": row.get("metaKeywords", "") if pd.notna(row.get("metaKeywords")) else "",
                "cover": int(row.get("cover", 0)) if pd.notna(row.get("cover")) else 0,
                "stay_ahead": int(row.get("stay_ahead")) if pd.notna(row.get("stay_ahead")) else None,
                "city": row.get("city", "") if pd.notna(row.get("city")) else "",
                "date": formatted_date  
            }
            print("Processed row:", article)  
            data.append({"data": article})
        print("Parsed data:", data)
        return data
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

def send_data(data):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    for item in data:
        filtered_data = {k: v for k, v in item['data'].items() if v not in [None, "", 0]}
        payload = {"data": filtered_data}
        
        print(f"Sending data: {payload}")
        try:
            response = requests.post(STRAPI_URL, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Successfully sent: {filtered_data['title']}")
        except requests.exceptions.RequestException as e:
            if e.response:
                print(f"Error with {filtered_data.get('title', 'Unknown')}:", e.response.text)
            else:
                print(f"Unknown error with {filtered_data.get('title', 'Unknown')}: {e}")

def watch_directory(directory):
    print(f"Watching for new CSV files in {directory}")
    while True:
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory, filename)
                print(f"New CSV file detected: {filename}")
                
                data = read_csv(file_path)
                if data:
                    send_data(data)
                    time.sleep(10) 
                    
                try:
                    os.remove(file_path)
                    print(f"Processed and deleted file: {filename}")
                except Exception as e:
                    print(f"Error deleting file {filename}: {e}")
        time.sleep(5)

watch_directory(WATCH_DIR)
