# Use the official Python image based on Debian Buster
FROM python:3.11-buster

WORKDIR /app

# Install Java 11
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64

# Copy project
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Run application
ENTRYPOINT ["python3", "main.py"]
CMD ["10"]