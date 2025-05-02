import json
from google.cloud import bigquery
from google.cloud import storage

def upload_to_bigquery(event, context):
    file_name = event['name']
    bucket_name = event['bucket']

    # Load JSON from GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_text()
    data = json.loads(content)

    if not isinstance(data, list):
        data = [data]

    client = bigquery.Client()
    table_id = "temp-calculation.data_temp.temp_data"
    dataset_id = "temp-calculation.data_temp"

    # Temporary table creation
    temp_table_id = f"{dataset_id}.temp_staging"
    schema = [
        bigquery.SchemaField("date_time", "TIMESTAMP"),
        bigquery.SchemaField("temperature", "FLOAT"),
        bigquery.SchemaField("water_level", "INT64"),
        bigquery.SchemaField("light_luminance", "INT64"),
        bigquery.SchemaField("ph_value", "FLOAT"),
    ]

    # Create temp table
    job_config = bigquery.LoadJobConfig(schema=schema)
    job = client.load_table_from_json(data, temp_table_id, job_config=job_config)
    job.result()
    print("✅ Loaded data to staging table.")

    # MERGE query (update or insert)
    merge_query = f"""
        MERGE `{table_id}` T
        USING `{temp_table_id}` S
        ON T.date_time = S.date_time
        WHEN MATCHED THEN
          UPDATE SET
            temperature = S.temperature,
            water_level = S.water_level,
            light_luminance = S.light_luminance,
            ph_value = S.ph_value
        WHEN NOT MATCHED THEN
          INSERT (date_time, temperature, water_level, light_luminance, ph_value)
          VALUES(S.date_time, S.temperature, S.water_level, S.light_luminance, S.ph_value)
    """
    client.query(merge_query).result()
    print("✅ Data merged (updated/inserted).")

    # DELETE rows not present in staging
    delete_query = f"""
        DELETE FROM `{table_id}`
        WHERE date_time NOT IN (SELECT date_time FROM `{temp_table_id}`)
    """
    client.query(delete_query).result()
    print("🗑️ Deleted rows not present in GCS JSON.")

    # Optional: Delete temp table
    client.delete_table(temp_table_id, not_found_ok=True)
