import json

import boto3
import botocore

BUCKET_NAME = "my-bucket"
ENDPOINT_URL = "http://localhost:4566"


# Create a bucket
s3_client =boto3.client('s3', config=boto3.session.Config(signature_version=botocore.UNSIGNED), endpoint_url=ENDPOINT_URL)



response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix="0/")

# Print all object names (keys)
if 'Contents' in response:
    for item in response['Contents']:
        print(item['Key'])
else:
    print(f"No items in bucket {BUCKET_NAME}")