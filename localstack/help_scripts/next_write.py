import boto3
import json

BUCKET_NAME = "myb"
FILE_NAME = "myfile.txt"
ENDPOINT_URL = "http://localhost:4566"

s3_client = boto3.client('s3', endpoint_url=ENDPOINT_URL)

# Create a bucket
s3_client.create_bucket(Bucket=BUCKET_NAME)

# Update bucket policy to grant public read access
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

# Enable Static Website Hosting
website_configuration = {
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}
s3_client.put_bucket_website(Bucket=BUCKET_NAME, WebsiteConfiguration=website_configuration)

# Optional: Set up CORS if needed
cors_configuration = {
    'CORSRules': [{
        'AllowedHeaders': ['*'],
        'AllowedMethods': ['GET'],
        'AllowedOrigins': ['*'],
        'ExposeHeaders': ['GET'],
        'MaxAgeSeconds': 3000
    }]
}
s3_client.put_bucket_cors(Bucket=BUCKET_NAME, CORSConfiguration=cors_configuration)

# Upload a file to the bucket
with open(FILE_NAME, "w") as f:
    f.write("This is a test file")

s3_client.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)