import boto3
from fastapi import HTTPException, UploadFile

from app.core.config import settings

S3_BUCKET_NAME = settings.AWS_S3_BUCKET
S3_REGION = settings.AWS_S3_REGION

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=S3_REGION,
)


def upload_file_to_s3(file: UploadFile, object_name: str = None) -> str:
    if S3_BUCKET_NAME is None:
        raise HTTPException(status_code=500, detail="S3_BUCKET_NAME is not configured.")

    if object_name is None:
        object_name = file.filename

    try:
        s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, object_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file to S3: {e}")

    file_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{object_name}"
    return file_url
