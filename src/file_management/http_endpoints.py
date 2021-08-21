from typing import Optional

import boto3
from fastapi import APIRouter, File, UploadFile
from fastapi.logger import logger

router = APIRouter()


@router.post("/file/upload", tags=["file", "upload"])
async def file_upload(file: UploadFile = File(...)) -> dict:
    content = await file.read()
    text_content: Optional[str] = None
    if isinstance(content, bytes):
        text_content = content.decode(encoding="utf-8")
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.put_object(
            Bucket="tanayseven.com-simple-bucket", Key=file.filename, Body=text_content
        )
    logger.info(f"{text_content}")
    return {"message": f"{file.filename} successfully uploaded"}
