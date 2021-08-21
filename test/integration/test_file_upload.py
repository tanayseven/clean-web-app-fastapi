from pathlib import Path

import boto3
from fastapi.testclient import TestClient
from moto import mock_s3  # type: ignore


@mock_s3
def test_file_upload(client: TestClient) -> None:
    conn = boto3.resource("s3", region_name="us-east-1")
    simple_bucket = "tanayseven.com-simple-bucket"
    conn.create_bucket(Bucket=simple_bucket)
    some_file = "some-file.txt"
    with open(Path(".") / "test" / "data" / some_file, "r") as file_handler:
        file_to_be_uploaded = {"file": (some_file, file_handler, "text/plain")}
        response = client.post("/file/upload", files=file_to_be_uploaded)
    assert response.json() == {"message": f"{some_file} successfully uploaded"}
    body = conn.Object(simple_bucket, some_file).get()["Body"].read().decode("utf-8")
    assert body == "This is some text that I want to save"
