# Connect to S3

import boto3, botocore
from app import app
# from config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

# Function to upload file to s3
def upload_file_to_s3(file, bucket_name, acl="public-read"):

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    
    print("{}{}".format(app.config["S3_LOCATION"], file.filename))

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)