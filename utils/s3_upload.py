import boto3, os, uuid
from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID ="AKIA3QFM6OASSNO4CHWQ" #os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = "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"#os.getenv
AWS_REGION = "eu-north-1"  # ou sua região
BUCKET_NAME = "app-panduline"

# Cliente S3
s3 = boto3.client("s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def upload_file(local_path: str) -> str:
    key = f"faces/{uuid.uuid4().hex}{os.path.splitext(local_path)[1]}"
    try:
        #s3.upload_file(local_path, S3_BUCKET, key, ExtraArgs={'ACL': 'public-read'})

        contents = await file.read()
        file_stream=io.BytesIO(contents)
        s3.upload_fileobj(
            Fileobj=file_stream,
            Bucket=BUCKET_NAME,
            Key=file.filename,
            ExtraArgs={"ContentType":file.content_type}
        )
        url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file.filename}"
        print(url)
        return {"url": url}
    except ClientError as e:
        raise RuntimeError(f"S3 upload failed: {e}")
    url = f"https://{S3_BUCKET}.s3.{REGION}.amazonaws.com/{key}"
    return url
