# 🖐️ Hand Detection Web Application (AWS Serverless)

A fully serverless web application built on AWS that allows users to upload an image, performs hand detection using MediaPipe, and returns detection results via an API.

This project demonstrates a production-style serverless architecture using AWS Lambda, S3, API Gateway, Docker, and AWS SAM.

---

## 📌 Architecture Overview

Flow of the application:

1. Client uploads an image using an HTTP POST request
2. API Gateway forwards the request to the Upload Lambda
3. Image is stored in an S3 bucket under `uploads/`
4. S3 event triggers the MediaPipe Lambda (container-based)
5. MediaPipe performs hand detection on the image
6. The output image will be save in s3 bucket under `results/`

Client → API Gateway → Upload Lambda → S3 → MediaPipe Lambda

---

## 🧱 Tech Stack

- AWS Lambda (ZIP + Container Image)
- Amazon API Gateway
- Amazon S3
- AWS SAM (Serverless Application Model)
- Docker & Amazon ECR
- MediaPipe (Hand Detection)
- Python 3.9

---

## 📂 Project Structure

```text
hand-detection-app/
├── template.yaml
├── samconfig.toml
├── upload_lambda_app/
│   ├── app.py
│   └── requirements.txt
├── mediapipe_lambda_app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── README.md
```


---

## 🚀 Features

- Image upload API
- Secure S3 storage
- MediaPipe hand detection
- Docker-based Lambda for ML workloads
- Infrastructure as Code with SAM
- Plug-and-play deployment

---

## 🛠 Prerequisites

Make sure the following are installed:

- AWS CLI (configured)
- AWS SAM CLI
- Docker
- Python 3.9+


---

🔐 AWS Permissions Required

Your IAM user or role must allow:

- CloudFormation
- IAM
- Lambda
- S3
- API Gateway
- ECR

For learning or development, AdministratorAccess is recommended.


🏗 Build and Deploy
Step 1: Clone the repository

```bash
git clone https://github.com/<your-username>/hand-detection-app.git
cd hand-detection-app
```
Step 2: Build the application, This builds both the ZIP-based upload Lambda and the Docker image for the MediaPipe Lambda.

```bash
sam build --use-container
```

Step 3: Deploy to AWS
```bash
sam deploy --guided
```
During setup:

- Stack name: hand-detection-app
- Region: choose your region
- Bucket-Name: 
- Allow SAM to create IAM roles: Yes
- Create managed ECR repositories: Yes

🌐 Get API Endpoint

After deployment, run:
```bash
sam list endpoints --stack-name hand-detection-app
```

Use this sample code to upload an image through an API
```bash

import requests
import base64, json

# 🔹 Replace with your API Gateway URL
API_URL=""
# 🔹 Path to image you want to upload
IMAGE_PATH = ""

with open(IMAGE_PATH, "rb") as f:
    img_bytes = f.read()


# Encode image as base64
img_b64 = base64.b64encode(img_bytes).decode("utf-8")

# Send JSON payload with isBase64Encoded flag
payload = {
    "body": img_b64,
    "isBase64Encoded": True
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
print("Status Code:", response.status_code)
print("Response:", response.text)
```

