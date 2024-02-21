# Distributed-PE-Processor

## Overview
This ETL (Extract, Transform, Load) project aims to extract metadata from Windows PE files stored in an S3 bucket, transform that data, and load it into a PostgreSQL database. 

## Project diagram
![spark_schema](https://github.com/adam-pawelek/Distributed-PE-Processor-ETL/assets/45467141/e0b713ae-76bb-461c-b7a3-54033305fbd4)


## Metadata Extracted
- File path and size
- File type (dll or exe)
- Architecture (x32 or x64)
- Number of imports (integer)
- Number of exports (integer)

## Technology Stack
- **PySpark**: Utilized for large-scale data processing. [Learn more](https://spark.apache.org/docs/latest/api/python/index.html)
- **Spark Cluster**: Comprises master and worker containers for distributed data processing. [Cluster Overview](https://spark.apache.org/docs/latest/cluster-overview.html) | [Setup Guide](https://medium.com/@MarinAgli1/setting-up-a-spark-standalone-cluster-on-docker-in-layman-terms-8cbdc9fdd14b)
- **Python pefile Library:** For extracting metadata from Windows PE files
- **PostgreSQL:** Database for storing extracted metadata
- **Docker:** For creating and managing the application and database environments
- **Elasticsearch, Logstash, Kibana (ELK stack):** For logging and log visualization

## Quick Start

### Prerequisites
1. Ensure Docker and Docker Compose are installed on your machine to build and run the necessary containers for the application, database, and ELK stack.<br>
2. **You have to have at least 10GB free ram to run the application.**
### Setup
#### Development Environment (lazy start one command and app is up and running)
1. **Environment Variables:**
   all environment variables are set in the docker-compose.dev.yaml file
2. **Build and Run Docker Containers:**
    - Navigate to the project directory and run the following command:
        ```sh
        docker compose -f docker-compose.dev.yaml up --build
        ```

#### Production Environment
1. **Environment Variables:** 
    - Create a `.env` file at the root of the project.
    - Fill the `.env` file with your specific configuration:
        ```plaintext
      DB_USER=db_user
      DB_PASSWORD=db_password
      DB_NAME=db_name
      BUCKET_NAME=your_s3_bucket_name
        ```
   
2. **Build and Run Docker Containers:**
    - Navigate to the project directory and run the following command:
        ```sh
        docker compose -f docker-compose.prod.yaml up --build
        ```
### Modifying Number of Downloaded Files
You can modify the number of files to be downloaded by adjusting the `CMD` value in the Docker Compose file. For instance:

   ```yaml
   python-app:
     build:
       context: .
       dockerfile: Dockerfile.spark.pythonS
     command: ["1000000"]
   ```
In your Dockerfile, you might have an entry similar to:
   ```
   ENTRYPOINT ["python3", "main.py"]
   CMD ["10000"]
   ```
This means by default 10000 files will be downloaded unless the command in the docker-compose.prod.yaml overrides it (as in the example where it's set to 1000000).
Attention: The number of files to be downloaded should be less than the number of files in the S3 bucket.

### Accessing the Applications
- **Spark Master Dashboard:** [http://localhost:8080/](http://localhost:8080/)
  
- **Kibana Dashboard:** [http://localhost:5601/app/home#/](http://localhost:5601/app/home#/)

- **Adminer (DB Viewer):** [http://localhost:8089/](http://localhost:8089/)

## Application Architecture

### Data Flow
1. **Extraction:** Retrieve Windows PE files from the specified S3 bucket.
2. **Transformation:** Extract the predefined metadata using PySpark and Python's pefile library.
3. **Load:** Store the transformed data into the PostgreSQL database.

### Logging
The application uses the ELK stack for logging:
- **Elasticsearch:** Stores logs
- **Logstash:** Processes logs
- **Kibana:** Visualizes logs on a dashboard

### Note
- The Kibana dashboard is unprotected and doesn't require any credentials for access. Ensure proper network configurations to secure your data.


---

# Localstack 
## Set up aws 
### Install aws cli on ubuntu 
```bash
sudo apt  install awscli 
```

## Configure AWS CLI
To interact with LocalStack, you need the AWS CLI tool installed on your machine. If you haven't installed it yet, you can download it from the AWS website.

### Creating Credentials:
LocalStack doesn't require real AWS credentials but uses dummy credentials. You can configure AWS CLI with any random credentials:

```bash
aws configure
```
When prompted, you can enter the following:

AWS Access Key ID: test <br>
AWS Secret Access Key: test <br>
Default region name: your preferred region (e.g., us-east-1) <br>
Default output format: json <br>

## Localstack S3 on localhost
### Create a Bucket
To create a bucket in LocalStack, use the AWS CLI command with the endpoint URL pointing to your LocalStack instance:

```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://my-bucket
```
Replace my-bucket with your desired bucket name.

### List Buckets
To list all the buckets:

```bash
aws --endpoint-url=http://localhost:4566 s3 ls
```

### List Bucket Contents
To list the contents of a bucket:

```bash
aws --endpoint-url=http://localhost:4566 s3 ls s3://my-bucket
```

### List all files in a bucket
To list all the files in a bucket:

```bash
aws --endpoint-url=http://localhost:4566 s3 ls s3://my-bucket --recursive
```

### Upload a File
To upload a file to the bucket:

```bash
aws --endpoint-url=http://localhost:4566 s3 cp /path/to/local/file s3://my-bucket
```
