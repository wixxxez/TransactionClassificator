import pandas as pd
from google.cloud import storage
import io
from datetime import datetime, timedelta
import google.auth 

def read_csv_from_gcs(path:str, index_col:int = None)->pd.DataFrame:
    """Download a CSV file from GCS and load it into Pandas DataFrame."""

    bucket_name, file_name = path.split('/')
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Download file as bytes
    csv_data = blob.download_as_bytes()

    # Read the CSV file into a Pandas DataFrame
    
    df = pd.read_csv(io.BytesIO(csv_data), index_col=index_col)
  
    return df



def upload_to_gcs(df: pd.DataFrame, path: str):
    """Uploads a file to Google Cloud Storage."""
    client = storage.Client()
    bucket_name, file_name = path.split('/')
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    # Upload CSV file to GCS
    blob.upload_from_string(csv_buffer.getvalue(), content_type="text/csv")

def save_html_to_gcs(html_content, path):
    """Saves an HTML file to Google Cloud Storage."""
    client = storage.Client()

    bucket_name, file_name = path.split('/')
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Upload the HTML content to GCS
    blob.upload_from_string(html_content, content_type="text/html")
    
def generate_signed_url(bucket_name, blob_name, expiration_minutes=15):
    """Generate a signed URL for a file in GCS (valid for limited time)."""

     
    client = storage.Client.from_service_account_json("/secrets/keyjson")
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Set expiration time
    expiration_time = timedelta(minutes=expiration_minutes)

    # Generate signed URL
    signed_url = blob.generate_signed_url(
        expiration=expiration_time,
        method="GET"
    )
    
    return signed_url
