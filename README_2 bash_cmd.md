Project Title
AFTER SUCCESFULLY INSATLLED CLI JUST RUN THIS BELOW COMMAND IN BASH - VSCODE

✅ STEP 1: Install Google Cloud CLI
Download and install CLI from: https://cloud.google.com/sdk/docs/install
After installation, initialize:
gcloud init

✅ STEP 2: Authenticate with your service account
Place your service-account-key.json in your project directory and run:
gcloud auth activate-service-account --key-file=service-account-key.json

✅ STEP 3: Set default project and region
gcloud config set project temp-calculation gcloud config set functions/region asia-south1

✅ STEP 4: Enable required APIs
gcloud services enable storage.googleapis.com gcloud services enable bigquery.googleapis.com gcloud services enable cloudfunctions.googleapis.com

✅ STEP 5: Create a Cloud Storage bucket
gsutil mb -p temp-calculation -l asia-south1 gs://bucket-tempreture

✅ STEP 6: Create BigQuery dataset and table
bq mk --dataset --location=asia-south1 temp-calculation:data_temp

Create BigQuery table schema (optional if using auto-schema detection)
bq mk --table temp-calculation:data_temp.temp_data
date_time:TIMESTAMP,temperature:FLOAT,water_level:INT64,light_luminance:INT64,ph_value:FLOAT

✅ STEP 7: Create Cloud Function
Ensure your function is in main.py with entry point upload_to_bigquery
and requirements.txt includes necessary libraries
gcloud functions deploy function-temp
--runtime python310
--trigger-resource bucket-tempreture
--trigger-event google.storage.object.finalize
--entry-point upload_to_bigquery
--region asia-south1
--allow-unauthenticated

✅ STEP 8: Run your upload script (infinite JSON upload to bucket)
Make sure upload.py is correct and uses service-account-key.json
python upload.py

✅ STEP 9: Connect BigQuery to Looker Studio
- Go to https://lookerstudio.google.com
- Create a new report → Add Data → Choose BigQuery
- Select your table: temp-calculation → data_temp → temp_data
- Create a Line Chart
- Add “date_time” as dimension, “temperature” as metric
- Apply filter:
➕ Add Filter → Create Filter → Include → date_time → is in the last → 1 Hour
✅ STEP 10: Optional - Embed Looker Studio with Auto-Refresh
- Publish your report → Get embed code
- Append &interval=60&autoRefresh=true to the URL for auto-refresh
Example Embed URL:
https://lookerstudio.google.com/embed/reporting/<REPORT_ID>/page/<PAGE_ID>?interval=60&autoRefresh=true
🎉 DONE!
You now have a real-time line chart showing IoT sensor data updating every 5 seconds in Looker Studio!
