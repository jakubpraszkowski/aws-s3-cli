# aws-s3-cli

# Usage
Before using app the shell needs to be configured using for aws credentials using *aws configure*

    usage: aws_cli.py [-h] [--list] [--upload UPLOAD] [--filter FILTER] [--delete DELETE] --bucket BUCKET --prefix PREFIX

    AWS S3 CLI Tool

      options:
        -h, --help       show this help message and exit
        --list           List all files in the S3 bucket.
        --upload UPLOAD  Upload a local file to the S3 bucket.
        --filter FILTER  List files matching the given regex pattern.
        --delete DELETE  Delete files matching the given regex pattern.
        --bucket BUCKET  S3 bucket name.
        --prefix PREFIX  S3 prefix.

        Examples:
        List files: python aws_cli.py --list --bucket my-bucket --prefix my-prefix/
        Upload a file: python aws_cli.py --upload /path/to/local/file --bucket my-bucket --prefix my-prefix/
        List files with filter: python aws_cli.py --filter '\.jpg$' --bucket my-bucket --prefix my-prefix/
        Delete files matching regex: python aws_cli.py --delete '\.jpg$' --bucket my-bucket --prefix my-prefix/