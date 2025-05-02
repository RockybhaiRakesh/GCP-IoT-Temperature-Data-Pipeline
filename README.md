Project Title
GCP IoT Temperature Data Pipeline with Looker Studio Dashboard

GCP IoT Temperature Data Pipeline with Looker Studio Dashboard
This project streams temperature and environment sensor data to Google Cloud Storage (GCS), transfers it into BigQuery using a Cloud Function, and visualizes it in Looker Studio.

📦 Requirements
Python 3.7+
Google Cloud SDK (CLI)
GCP Billing-enabled project
IAM roles: Storage Admin, BigQuery Admin, Cloud Functions Admin
⚙️ Step 1: Install Google Cloud CLI
# Install CLI (Linux/macOS)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# For Windows: Use the official installer from:
# https://cloud.google.com/sdk/docs/install

# Initialize
gcloud init
🗝️ Step 2: Authenticate with GCP
# Create service account key
# Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
# -> Create Key -> JSON -> Download

# Set env var (optional)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
🪣 Step 3: Create GCS Bucket
# Replace with your bucket name and location
BUCKET_NAME="bucket-tempreture"
gcloud storage buckets create $BUCKET_NAME \
  --location=us-central1 \
  --project=[YOUR_PROJECT_ID]
🧠 Step 4: Create BigQuery Dataset & Table
# Create Dataset
gcloud bigquery datasets create data_temp

# Create Table
bq mk --table \
  data_temp.temp_data \
  date_time:TIMESTAMP,temperature:FLOAT,water_level:INTEGER,light_luminance:INTEGER,ph_value:FLOAT
🧩 Step 5: Deploy Cloud Function
# Enable required services
gcloud services enable cloudfunctions.googleapis.com

# Deploy
cd [your_project_folder_with_main.py]
gcloud functions deploy upload_to_bigquery \
  --runtime python310 \
  --trigger-resource $BUCKET_NAME \
  --trigger-event google.storage.object.finalize \
  --entry-point upload_to_bigquery \
  --source=. \
  --region=us-central1 \
  --set-env-vars GOOGLE_APPLICATION_CREDENTIALS="service-account-key.json"
💻 Step 6: Run Data Generator (upload.py)
# Install dependencies
pip install -r requirements.txt

# Run the data uploader
python upload.py
This script will:

Generate random temperature/environment data every 5 seconds
Upload to temp_data.json in your GCS bucket continuously
📊 Step 7: Create Looker Studio Dashboard
Go to: https://lookerstudio.google.com

Create a new report

Data Source → BigQuery → your dataset: data_temp.temp_data

Create a Line Chart with:

X-Axis: date_time
Y-Axis: temperature / water_level / etc.
Add a Filter:

date_time is in the last 1 hour
Enable auto-refresh in Embed code:

<meta http-equiv="refresh" content="30"> <!-- every 30 sec -->
📂 File Structure
project_folder/
├── main.py               # Cloud Function to load GCS JSON to BigQuery
├── upload.py             # IoT-like script to send JSON to GCS
├── requirements.txt      # pip dependencies
└── service-account-key.json
📚 Notes
You can extend upload.py to include more sensors.
Looker Studio doesn’t support real-time streaming — only simulates it using refresh.
✅ requirement.txt
google-cloud-storage
google-cloud-bigquery
google-auth
🔚 End
Now you have a live-like temperature monitoring dashboard using GCS, BigQuery, Cloud Functions, and Looker Studio!