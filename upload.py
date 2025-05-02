import os
import json
import random
import time
from datetime import datetime, timedelta
from google.cloud import storage
from google.oauth2 import service_account

# Set credentials
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(BASE_DIR, 'service-account-key.json')
creds = service_account.Credentials.from_service_account_file(credentials_path)

# GCS client
storage_client = storage.Client(credentials=creds, project=creds.project_id)

# Config
BUCKET_NAME = "bucket-tempreture"
DEST_BLOB = "temp_data.json"

# ✅ Start from current time
current_time = datetime.now()

# Initialize data list
data = []

print("🚀 Starting infinite data generation and upload. Press Ctrl + C to stop.\n")

try:
    while True:
        # Generate new record
        record = {
            "date_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": round(random.uniform(10.0, 35.0), 2),
            "water_level": random.randint(100, 300),
            "light_luminance": random.randint(100, 500),
            "ph_value": round(random.uniform(5.0, 14.0), 2)
        }

        # Append to list
        data.append(record)

        # Upload full data array to GCS
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(DEST_BLOB)
        blob.upload_from_string(data=json.dumps(data), content_type="application/json")
        print(f"✅ Appended and uploaded record with time {record['date_time']}")

        # Wait and increment time
        time.sleep(5)
        current_time += timedelta(seconds=5)

except KeyboardInterrupt:
    print("\n🛑 Upload stopped by user.")
