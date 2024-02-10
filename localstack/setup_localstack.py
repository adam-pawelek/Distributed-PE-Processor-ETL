import json
import os
import sys

import boto3

from dotenv import load_dotenv

import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Example messages
logging.debug('This is a debug message\n\n\n\n\n')
logging.info('This is an info message\n\n\n\n\n')

load_dotenv()


BUCKET_NAME = os.getenv("BUCKET_NAME") #"my-bucket-test"
ENDPOINT_URL = os.getenv("ENDPOINT_URL")# "http://localhost:4566"

s3_client = boto3.client('s3', endpoint_url=ENDPOINT_URL)

# Create a bucket
s3_client.create_bucket(Bucket=BUCKET_NAME)

logging.info('\n\n\n\nCreated bucket \n\n\n\n\n')

# Make the bucket public
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject", "s3:GetObjectVersion"],
            "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"
        }
    ]
}
policy_json = json.dumps(bucket_policy)
s3_client.put_bucket_policy(Bucket=BUCKET_NAME, Policy=policy_json)

logging.info('\n\n\n\n\n put_bucket_policy \n\n\n\n\n')
def upload_files_to_s3(local_directory, bucket, destination):
    """
    Upload files from a local directory to an S3 bucket.

    :param local_directory: Local directory to upload files from.
    :param bucket: Name of the S3 bucket.
    :param destination: The destination folder in the S3 bucket.
    """
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = os.path.join(destination, relative_path)

            print(f"Uploading {local_path} to {s3_path}")
            s3_client.upload_file(local_path, bucket, s3_path)

# Replace '0' with the path to your local directory if it's different
local_directory = '0'



# S3 destination folder
s3_destination = '0'

# Upload files
upload_files_to_s3(local_directory, BUCKET_NAME, s3_destination)

logging.info('\n\n\n\n\n upload_files_to_s3 \n\n\n\n\n')

local_directory = '1'



# S3 destination folder
s3_destination = '1'

# Upload files
upload_files_to_s3(local_directory, BUCKET_NAME, s3_destination)