import boto3
import botocore

# Set the endpoint URL to the S3 website endpoint
ENDPOINT_URL = None

# Initialize the S3 client
s3_client = boto3.client('s3', config=boto3.session.Config(signature_version=botocore.UNSIGNED), endpoint_url=ENDPOINT_URL)

# Specify the S3 bucket name
bucket_name = 's3-nord-challenge-data'

# List the first 10 objects in the bucket
response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=10)

# Print the list of object keys (i.e., file names)
for obj in response.get('Contents', []):
    print(obj['Key'])