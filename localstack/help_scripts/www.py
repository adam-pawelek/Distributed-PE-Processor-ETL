import json

import boto3

# Bucket and file names
BUCKET_NAME = "bucket"
INDEX_FILE_NAME = "index.html"
FILE_NAME = "myfile.txt"
ENDPOINT_URL = "http://localhost:4566"

# HTML content for index.html
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>My Bucket Files</title>
</head>
<body>
    <h1>Files in My Bucket</h1>
    <ul>
        <li><a href="{file_name}" download>Download {file_name}</a></li>
        <!-- Add more files as needed -->
    </ul>
</body>
</html>
""".format(file_name=FILE_NAME)

# Write HTML content to index.html
with open(INDEX_FILE_NAME, "w") as f:
    f.write(html_content)

# Initialize S3 client
s3_client = boto3.client('s3', endpoint_url=ENDPOINT_URL)

# Create the bucket if it doesn't exist
try:
    s3_client.create_bucket(Bucket=BUCKET_NAME)
except s3_client.exceptions.BucketAlreadyOwnedByYou:
    pass  # Bucket already exists, no need to create it

# Upload the index.html file
s3_client.upload_file(INDEX_FILE_NAME, BUCKET_NAME, INDEX_FILE_NAME)

# Upload myfile.txt for testing purposes
with open(FILE_NAME, "w") as f:
    f.write("This is a test file")
s3_client.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)

# Update the bucket policy to allow public read access
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
    'IndexDocument': {'Suffix': INDEX_FILE_NAME},
}
s3_client.put_bucket_website(Bucket=BUCKET_NAME, WebsiteConfiguration=website_configuration)
