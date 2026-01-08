import json
import boto3
import base64
import uuid
import os

s3 = boto3.client('s3')
BUCKET_NAME = os.environ["UPLOAD_BUCKET"]   #"hand-detection-uploads-sheraz"

def lambda_handler(event, context):
    try:
        # event['body'] is already base64 string from JSON
        img_b64 = json.loads(event['body'])['body']
        body = base64.b64decode(img_b64)

        file_name = f"uploads/{uuid.uuid4()}.jpg"
        s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=body, ContentType="image/jpeg")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Image uploaded successfully", "file": file_name})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
