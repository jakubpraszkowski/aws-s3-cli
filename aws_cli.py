import argparse
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
    print(f"Listing files in bucket: {bucket_name}, prefix: {prefix}")
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' in response:
            for obj in response['Contents']:
                print(obj['Key'])
        else:
            print("No files found.")
    except Exception as e:
        print(f"Failed to list files: {e}")


def upload_file(bucket_name, prefix, local_file_path):
    key = os.path.join(prefix, os.path.basename(local_file_path))

    print(f"Uploading {local_file_path} to {key}")
    try:
        s3_client.upload_file(local_file_path, bucket_name, key)
        print("Upload completed.")
    except Exception as e:
        print(f"Failed to upload {local_file_path}: {e}")


def list_files_with_filter(bucket_name, prefix, regex_pattern):
    print(f"Listing files matching pattern: {regex_pattern}")
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' in response:
            for obj in response['Contents']:
                if re.search(regex_pattern, obj['Key']):
                    print(obj['Key'])
        else:
            print("No files found.")
    except Exception as e:
        print(f"Failed to list files: {e}")


def delete_files_matching_regex(bucket_name, prefix, regex_pattern):
    print(f"Deleting files matching pattern: {regex_pattern}")
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        pattern = re.compile(regex_pattern)
        if 'Contents' in response:
            for obj in response['Contents']:
                if pattern.search(obj['Key']):
                    print(f"Deleting {obj['Key']}")
                    s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
        else:
            print("No files found.")
    except Exception as e:
        print(f"Error deleting files: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="AWS S3 CLI Tool",
        epilog="""
        Examples:
        List files: python aws_cli.py --list --bucket my-bucket --prefix my-prefix/
        Upload a file: python aws_cli.py --upload /path/to/local/file --bucket my-bucket --prefix my-prefix/
        List files with filter: python aws_cli.py --filter '\\.jpg$' --bucket my-bucket --prefix my-prefix/
        Delete files matching regex: python aws_cli.py --delete '\\.jpg$' --bucket my-bucket --prefix my-prefix/
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--list', action='store_true', help="List all files in the S3 bucket.")
    parser.add_argument('--upload', type=str, help="Upload a local file to the S3 bucket.")
    parser.add_argument('--filter', type=str, help="List files matching the given regex pattern.")
    parser.add_argument('--delete', type=str, help="Delete files matching the given regex pattern.")
    parser.add_argument('--bucket', type=str, required=True, help="S3 bucket name.")
    parser.add_argument('--prefix', type=str, required=True, help="S3 prefix.")

    args = parser.parse_args()

    if args.list:
        list_files(args.bucket, args.prefix)
    elif args.upload:
        upload_file(args.bucket, args.prefix, args.upload)
    elif args.filter:
        list_files_with_filter(args.bucket, args.prefix, args.filter)
    elif args.delete:
        delete_files_matching_regex(args.bucket, args.prefix, args.delete)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()