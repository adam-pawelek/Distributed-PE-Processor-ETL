FROM docker.io/bitnami/spark:3.5

USER root
WORKDIR /opt/bitnami/spark/jars

ENV POSTGRES_JDBC_VERSION=42.2.23


RUN apt-get update && \
    apt-get install -y  wget &&\
    wget https://jdbc.postgresql.org/download/postgresql-${POSTGRES_JDBC_VERSION}.jar &&\
    wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar &&\
    wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.3.4/hadoop-common-3.3.4.jar &&\
    wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar


WORKDIR /app

COPY distributed_pe_processor distributed_pe_processor
COPY setup.py setup.py

RUN pip install --upgrade pip

#install distributed_pe_processor package
RUN python3 setup.py sdist && \
    pip3 install dist/distributed_pe_processor-0.1.tar.gz







