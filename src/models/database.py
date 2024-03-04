import os
import uuid
from decimal import Decimal
import boto3

from src.analysis.full_analysis import compute_full_analysis

# To configure the below locally on a command prompt in Windows, do:
'''
set AWS_ACCESS_KEY_ID=...
set AWS_SECRET_ACCESS_KEY=...
set AWS_REGION=us-east-1
set DYNAMODB_TABLE_NAME=textplorer-nosql-db
'''
# Initialize DynamoDB client with environment variables
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = os.environ.get('AWS_REGION')
dynamodb_table = os.environ.get('DYNAMODB_TABLE_NAME')

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb',
                          region_name=aws_region,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

# Get reference to the DynamoDB table
table = dynamodb.Table(dynamodb_table)


# Function to insert text analysis results into the DynamoDB table
def insert_analysis_results(analysis_results: dict, input_requestid: uuid.UUID):
    # the key must be 'requestid' since our dynamodb partition key is set "requestid (String)"
    requestid = str(input_requestid)
    analysis_results['requestid'] = requestid
    for key, value in analysis_results.items():
        if isinstance(value, float):
            analysis_results[key] = Decimal(str(value))
    response = table.put_item(Item=analysis_results)
    print("Analysis results inserted successfully:")
    print(response)


def fetch_database_info():
    # return a dictionary containing some dynamodb db table information
    database_dict = {'database_table_name': dynamodb_table, 'aws_region': aws_region}
    table = dynamodb.Table(dynamodb_table)
    response = table.scan(Select='COUNT')
    total_count = response['Count']
    database_dict['total_rows_data'] = total_count
    return database_dict

# sample_text = """
# A file system is a method an operating system uses to store, organize, and manage files and directories on a storage device.
# Some common types of file systems include: FAT (File Allocation Table): An older file system used by older versions of Windows and other operating systems.
# NTFS (New Technology File System): A modern file system used by Windows. It supports features such as file and folder permissions, compression, and encryption. ext (Extended File System):
# A file system commonly used on Linux and Unix-based operating systems. HFS (Hierarchical File System): A file system used by macOS. APFS (Apple File System):
# A new file system introduced by Apple for their Macs and iOS devices.
# """
#
# analysis_results = compute_full_analysis(sample_text)
#
# # Insert analysis results into the DynamoDB table
# insert_analysis_results(analysis_results)
