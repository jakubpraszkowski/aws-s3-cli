import os
import re
import boto3

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


def list_files(bucket_name, prefix):
    print("Listing files in bucket...")
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj['Key'])
    else:
        print("No files found.")


def upload_file(bucket_name, prefix, local_file_path):
    key = os.path.join(prefix, os.path.basename(local_file_path))
    
    try:
        print(f"Uploading {local_file_path} to {key}")
        s3_client.upload_file(local_file_path, bucket_name, key)
    
    except Exception as e:
        print(f"Failed to upload {local_file_path}: {e}")
    
    else:
        print("Upload completed.")


def list_files_with_filter(bucket_name, prefix, regex_pattern):
    print(f"Listing files matching pattern: {regex_pattern}")
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' in response:
        for obj in response['Contents']:
            if re.search(regex_pattern, obj['Key']):
                print(obj['Key'])
    else:
        print("No files found.")


def delete_files_matching_regex(bucket_name, prefix, regex_pattern):
    print(f"Deleting files matching pattern: {regex_pattern}")
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    pattern = re.compile(regex_pattern)
    if 'Contents' in response:
        for obj in response['Contents']:
            if pattern.search(obj['Key']):
                print(f"Deleting {obj['Key']}")
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
    else:
        print("No files found.")


def main():
    BUCKET_NAME = 'developer-task'
    PREFIX = 'a-wing/'
    
    list_files(BUCKET_NAME, PREFIX)
    # upload_file(BUCKET_NAME, PREFIX, 'a-wing/README.md')
    delete_files_matching_regex(BUCKET_NAME, PREFIX, r'\.md$')
    list_files_with_filter(BUCKET_NAME, PREFIX, r'\.md$')

if __name__ == "__main__":
    main()
