import os
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


def main():
    list_files()


if __name__ == "__main__":
    main()
