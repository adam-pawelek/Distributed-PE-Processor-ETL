import json

import boto3

BUCKET_NAME = "my-bucket"
FILE_NAME = "myfile.txt"
ENDPOINT_URL = "http://localhost:4566"

s3_client = boto3.client('s3', endpoint_url=ENDPOINT_URL)

# Create a bucket
s3_client.create_bucket(Bucket=BUCKET_NAME)

# Make the bucket public
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AddPublicReadAccess",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"
        }
    ]
}

# Download a file from the bucket
s3_client.download_file(BUCKET_NAME, FILE_NAME, FILE_NAME)


response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)

# Print all object names (keys)
if 'Contents' in response:
    for item in response['Contents']:
        print(item['Key'])
else:
    print(f"No items in bucket {BUCKET_NAME}")