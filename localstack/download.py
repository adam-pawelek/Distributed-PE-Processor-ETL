import boto3
import botocore
from botocore.exceptions import NoCredentialsError

BUCKET_NAME = "my-bucket"  # replace with your bucket name
FILE_NAME = "0/0efb5DodbKCV2ELUQMqhYaVUk6iOIwlA.dll"  # replace with the name of your file
LOCAL_FILE_PATH = "0efb5DodbKCV2ELUQMqhYaVUk6iOIwlA.dll"  # replace with the local path where you want to save the file
ENDPOINT_URL = "http://localhost:4566"  # the endpoint URL

def download_file():
    # Create an S3 client
    s3 = boto3.client('s3', endpoint_url=ENDPOINT_URL,  config=boto3.session.Config(signature_version=botocore.UNSIGNED))

    try:
        # Download the file
        s3.download_file(BUCKET_NAME, FILE_NAME, LOCAL_FILE_PATH)
        print(f"Downloaded {FILE_NAME} from bucket {BUCKET_NAME} to {LOCAL_FILE_PATH}")
    except NoCredentialsError:
        print("Credentials not available")

download_file()