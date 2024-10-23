import os
import re
import boto3

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

BUCKET_NAME = 'developer-task'
PREFIX = 'a-wing/'

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


def list_files():
    print("Listing files in bucket...")
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj['Key'])
    else:
        print("No files found.")


def upload_file(local_file_path):
    key = os.path.join(PREFIX, os.path.basename(local_file_path))
    
    try:
        print(f"Uploading {local_file_path} to {key}")
        s3_client.upload_file(local_file_path, BUCKET_NAME, key)
    
    except Exception as e:
        print(f"Failed to upload {local_file_path}: {e}")
    
    else:
        print("Upload completed.")


def list_files_with_filter(path, regex_pattern):
    print(f"Listing files matching pattern: {regex_pattern}")
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
    pattern = re.compile(regex_pattern)
    if 'Contents' in response:
        for obj in response['Contents']:
            if re.search(regex_pattern, obj['Key']):
                print(obj['Key'])
    else:
        print("No files found.")


def main():
    # upload_file('README.md')
    list_files()
    list_files_with_filter('a-wing/', r'\.jpg$')


if __name__ == "__main__":
    main()
