from setuptools import setup, find_packages

setup(
    name='distributed_pe_processor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pefile==2023.2.7',
        'py4j==0.10.9.7',
        'pyspark==3.5.0',
        'python-dotenv',
        'findspark',
        'psycopg2-binary',
        'python-logstash-async',
        'elasticsearch',
        'boto3==1.28.57',
        'botocore==1.31.57',
    ],
    author='Adam Pawelek',
    description='A distributed PE processor module designed to work with PySpark',
    url='https://github.com/adam-pawelek/Distributed-PE-Processor',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='pyspark distributed processing',
    python_requires='>=3.6',
)