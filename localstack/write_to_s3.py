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
policy_json = json.dumps(bucket_policy)
s3_client.put_bucket_policy(Bucket=BUCKET_NAME, Policy=policy_json)

# Upload a file to the bucket
with open(FILE_NAME, "w") as f:
    f.write("This is a test file")

s3_client.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)