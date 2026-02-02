# MNIST CNN Pipeline — Docker + AWS + CI/CD

A fully containerized ML pipeline that trains a CNN on MNIST and serves predictions via a REST API. Each stage (data, training, serving) runs in its own Docker container. Training runs on a GPU EC2 instance that terminates after completion. Serving runs on a long-lived CPU EC2 instance. All artifacts flow through S3. For MLOps benchmarking in electronics components manufacturer, refer to this website: https://github.com/minjilee-purdue/minjilee-purdue.github.io/edit/main/internships/LGInnotek//mlops_manufacturing_analysis.docx.pdf




https://github.com/user-attachments/assets/9de72954-833a-42d3-9f78-d5a592d70e32





---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Full Pipeline Flow](#full-pipeline-flow)
4. [Code](#code)
   - [1. Data Stage](#1-data-stage-data)
   - [2. Training Stage](#2-training-stage-train)
   - [3. Serving Stage](#3-serving-stage-serve)
   - [4. EC2 Bootstrap Script](#4-ec2-bootstrap-script-infra)
   - [5. CI/CD Pipeline](#5-cicd-pipeline-github-workflows)
   - [6. Tests](#6-tests)
   - [7. Docker Compose (Local Dev)](#7-docker-compose-local-dev-only)
5. [Cost Breakdown](#cost-breakdown)
6. [Prerequisites](#prerequisites)
7. [How to Run Locally](#how-to-run-locally)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   GitHub Actions                     │
│                                                     │
│  1. Run tests (pytest)                              │
│  2. Build & push images → AWS ECR                   │
│  3. Run data prep (lightweight, runs in Actions)    │
│  4. Trigger training on EC2 (GPU)                   │
│  5. On success → deploy serve image to EC2 (CPU)   │
└───────────┬─────────────────────┬───────────────────┘
            │                     │
            ▼                     ▼
┌───────────────────┐   ┌───────────────────────┐
│  EC2 (GPU)        │   │  EC2 (CPU)            │
│  Training         │   │  Serving              │
│                   │   │                       │
│  - Pull image     │   │  - Pull image         │
│    from ECR       │   │    from ECR           │
│  - Pull data      │   │  - Pull model         │
│    from S3        │   │    from S3            │
│  - Train CNN      │   │  - Run FastAPI        │
│  - Eval accuracy  │   │  - Expose port 8000   │
│  - Push model     │   │                       │
│    to S3          │   │                       │
│  - Terminate      │   │                       │
│    instance       │   │                       │
└───────────────────┘   └───────────────────────┘
            │                     ▲
            └─────────┬───────────┘
                      ▼
              ┌───────────────┐
              │   AWS S3      │
              │               │
              │  /data/       │  ← preprocessed data
              │  /model/      │  ← trained model + metadata
              └───────────────┘
```

---

## Project Structure

```
mnist-cnn-pipeline/
├── data/
│   ├── Dockerfile
│   └── preprocess.py              # Download, preprocess, upload to S3
├── train/
│   ├── Dockerfile
│   ├── train.py                   # Train CNN, save model to S3
│   └── model_eval.py              # Evaluate accuracy, gate the pipeline
├── serve/
│   ├── Dockerfile
│   └── app.py                     # FastAPI app, pulls model from S3 on startup
├── tests/
│   ├── test_train.py              # Unit tests for model structure
│   └── test_serve.py              # Unit tests for serving endpoints
├── infra/
│   └── ec2_launch.sh              # User-data script to bootstrap EC2 instances
├── docker-compose.yml             # For local development only
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # GitHub Actions pipeline
└── README.md
```

---

## Full Pipeline Flow

```
Push to main
       │
       ▼
┌─ Stage 1 ─┐   pytest passes?
│   Test     │──── No  → Stop
└────────────┘──── Yes ↓

┌─ Stage 2 ─┐   Build docker images
│   Build   │   Push to ECR
└────────────┘──── ↓

┌─ Stage 3 ─┐   Run data container (in Actions)
│   Data    │   Upload preprocessed data → S3
└────────────┘──── ↓

┌─ Stage 4 ─┐   Launch GPU EC2 (p3.2xlarge)
│   Train   │   Pull data from S3 → train CNN
│           │   Eval accuracy → fails? Pipeline stops
│           │   Push model → S3
│           │   Terminate GPU instance
└────────────┘──── ↓

┌─ Stage 5 ─┐   Launch CPU EC2 (t3.medium)
│  Deploy   │   Pull model from S3 on startup
│           │   Serve predictions on port 8000
└────────────┘
```

---

## Code

---

### 1. Data Stage (`data/`)

#### `data/preprocess.py`

```python
import tensorflow as tf
import numpy as np
import boto3
import io

S3_BUCKET = "your-mnist-pipeline-bucket"


def upload_to_s3(array, key):
    buf = io.BytesIO()
    np.save(buf, array)
    buf.seek(0)
    boto3.client("s3").put_object(Bucket=S3_BUCKET, Key=key, Body=buf)


def main():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    # Normalize + reshape for CNN input (batch, 28, 28, 1)
    x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
    x_test  = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0

    upload_to_s3(x_train, "data/x_train.npy")
    upload_to_s3(y_train, "data/y_train.npy")
    upload_to_s3(x_test,  "data/x_test.npy")
    upload_to_s3(y_test,  "data/y_test.npy")
    print("All data uploaded to S3.")


if __name__ == "__main__":
    main()
```

#### `data/Dockerfile`

```dockerfile
FROM python:3.11-slim
RUN pip install tensorflow numpy boto3
COPY preprocess.py .
ENTRYPOINT ["python", "preprocess.py"]
```

> This container is lightweight enough to run directly in GitHub Actions — no EC2 needed for this stage.

---

### 2. Training Stage (`train/`)

#### `train/train.py`

```python
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import boto3
import io
import json


S3_BUCKET = "your-mnist-pipeline-bucket"


def download_from_s3(key):
    buf = io.BytesIO()
    boto3.client("s3").download_fileobj(S3_BUCKET, key, buf)
    buf.seek(0)
    return np.load(buf)


def upload_model_to_s3(model, meta):
    # Save model locally first, then upload
    model.save("/tmp/cnn_mnist.keras")
    boto3.client("s3").upload_file(
        "/tmp/cnn_mnist.keras", S3_BUCKET, "model/cnn_mnist.keras"
    )

    # Upload training metadata
    boto3.client("s3").put_object(
        Bucket=S3_BUCKET,
        Key="model/train_meta.json",
        Body=json.dumps(meta),
    )


def build_cnn():
    return models.Sequential([
        layers.Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation="relu"),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation="relu"),
        layers.Dense(10, activation="softmax"),
    ])


def main():
    # Pull preprocessed data from S3
    x_train = download_from_s3("data/x_train.npy")
    y_train = download_from_s3("data/y_train.npy")

    model = build_cnn()
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    history = model.fit(
        x_train, y_train, epochs=5, batch_size=64, validation_split=0.1
    )

    val_acc = history.history["val_accuracy"][-1]
    meta = {"val_accuracy": val_acc}

    # Push trained model + metadata to S3
    upload_model_to_s3(model, meta)
    print(f"Training complete. Val Accuracy: {val_acc:.4f}")


if __name__ == "__main__":
    main()
```

#### `train/model_eval.py`

```python
import boto3
import json
import sys

S3_BUCKET = "your-mnist-pipeline-bucket"
ACCURACY_THRESHOLD = 0.95


def main():
    obj = boto3.client("s3").get_object(
        Bucket=S3_BUCKET, Key="model/train_meta.json"
    )
    meta = json.loads(obj["Body"].read())

    acc = meta["val_accuracy"]
    print(f"Validation Accuracy: {acc:.4f} (threshold: {ACCURACY_THRESHOLD})")

    if acc < ACCURACY_THRESHOLD:
        print("FAIL: Accuracy below threshold. Pipeline will stop.")
        sys.exit(1)  # Non-zero exit code stops the CI/CD pipeline
    else:
        print("PASS: Model approved for deployment.")


if __name__ == "__main__":
    main()
```

#### `train/Dockerfile`

```dockerfile
FROM tensorflow/tensorflow:2.15.0-gpu
RUN pip install boto3
COPY train.py model_eval.py .
ENTRYPOINT ["sh", "-c", "python train.py && python model_eval.py"]
```

> Uses the GPU base image. `train.py` runs first — if it succeeds, `model_eval.py` checks accuracy. A failed eval exits with code 1, which stops the entire pipeline.

---

### 3. Serving Stage (`serve/`)

#### `serve/app.py`

```python
import tensorflow as tf
import numpy as np
import boto3
from fastapi import FastAPI, UploadFile
from PIL import Image
import io
import os

app = FastAPI()

S3_BUCKET = "your-mnist-pipeline-bucket"
MODEL_PATH = "/tmp/cnn_mnist.keras"


def load_model_from_s3():
    """Pull the trained model from S3 on container startup."""
    if not os.path.exists(MODEL_PATH):
        print("Downloading model from S3...")
        boto3.client("s3").download_file(
            S3_BUCKET, "model/cnn_mnist.keras", MODEL_PATH
        )
        print("Model downloaded.")
    return tf.keras.models.load_model(MODEL_PATH)


# Load model once at startup — not on every request
model = load_model_from_s3()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile):
    img = Image.open(io.BytesIO(await file.read())).convert("L")
    img = img.resize((28, 28))
    arr = np.array(img).reshape(1, 28, 28, 1).astype("float32") / 255.0

    pred = model.predict(arr)
    digit = int(np.argmax(pred))
    confidence = float(np.max(pred))

    return {"digit": digit, "confidence": round(confidence, 4)}
```

#### `serve/Dockerfile`

```dockerfile
FROM python:3.11-slim
RUN pip install tensorflow numpy fastapi uvicorn pillow boto3
COPY app.py .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

> CPU-only image. The model is downloaded from S3 once at startup, so each `/predict` request has no extra latency.

---

### 4. EC2 Bootstrap Script (`infra/`)

#### `infra/ec2_launch.sh`

```bash
#!/bin/bash
# This script is passed as "User Data" when launching an EC2 instance.
# It automatically pulls and runs the correct container on startup.
# The IMAGE_NAME environment variable is injected via EC2 launch parameters.

set -e

# Install Docker
yum update -y
yum install -y docker
service docker start
usermod -a -G docker ec2-user

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Pull and run the target image
# IMAGE_NAME is set differently for training vs serving instances
docker pull $IMAGE_NAME
docker run -d --name app -p 8000:8000 $IMAGE_NAME
```

> Replace `<YOUR_ACCOUNT_ID>` with your actual AWS account ID. The `-p 8000:8000` flag only matters for the serving instance but is harmless on the training instance.

---

### 5. CI/CD Pipeline (`.github/workflows/`)

#### `.github/workflows/ci-cd.yml`

```yaml
name: CNN MNIST Pipeline (AWS)

on:
  push:
    branches: [main]

env:
  AWS_REGION: us-east-1
  ECR_REGISTRY: <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
  S3_BUCKET: your-mnist-pipeline-bucket

jobs:
  # ─── Stage 1: Test ──────────────────────────────────────────
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: |
          pip install tensorflow numpy fastapi httpx pillow pytest boto3
          pytest tests/

  # ─── Stage 2: Build & Push Images to ECR ────────────────────
  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id:     ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region:            ${{ env.AWS_REGION }}

      - uses: aws-actions/amazon-ecr-login@v2

      - run: |
          docker build -t $ECR_REGISTRY/data:latest  ./data
          docker build -t $ECR_REGISTRY/train:latest ./train
          docker build -t $ECR_REGISTRY/serve:latest ./serve

          docker push $ECR_REGISTRY/data:latest
          docker push $ECR_REGISTRY/train:latest
          docker push $ECR_REGISTRY/serve:latest

  # ─── Stage 3: Run Data Preprocessing ────────────────────────
  # Lightweight — runs directly in GitHub Actions, no EC2 needed.
  run-data:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id:     ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region:            ${{ env.AWS_REGION }}

      - run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
          docker run --rm \
            -e AWS_ACCESS_KEY_ID=${{ secrets.AWS_ACCESS_KEY_ID }} \
            -e AWS_SECRET_ACCESS_KEY=${{ secrets.AWS_SECRET_ACCESS_KEY }} \
            $ECR_REGISTRY/data:latest

  # ─── Stage 4: Launch GPU EC2 for Training ───────────────────
  train:
    runs-on: ubuntu-latest
    needs: run-data
    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id:     ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region:            ${{ env.AWS_REGION }}

      # Launch a GPU instance
      - run: |
          INSTANCE_ID=$(aws ec2 run-instances \
            --image-id ami-XXXXXXXX \
            --instance-type p3.2xlarge \
            --key-name my-keypair \
            --security-group-ids sg-XXXXXXXX \
            --iam-instance-profile Name=EC2-ECR-S3-Role \
            --user-data file://infra/ec2_launch.sh \
            --tag-specifications 'ResourceType=instance,TagSpecifications=[{Key=Name,Value=mnist-train}]' \
            --query 'Instances[0].InstanceId' --output text)
          echo "INSTANCE_ID=$INSTANCE_ID" >> $GITHUB_ENV

      # Poll S3 until the model file appears (training is done)
      - run: |
          echo "Waiting for model to appear in S3..."
          for i in $(seq 1 60); do
            if aws s3api head-object --bucket $S3_BUCKET --key model/train_meta.json 2>/dev/null; then
              echo "Model found. Training complete."
              exit 0
            fi
            echo "Waiting... ($i/60)"
            sleep 30
          done
          echo "FAIL: Training timed out after 30 minutes."
          exit 1

      # Terminate the GPU instance to stop billing
      - run: |
          aws ec2 terminate-instances --instance-ids $INSTANCE_ID
          echo "GPU instance terminated."

  # ─── Stage 5: Deploy Serving Instance (CPU) ─────────────────
  deploy:
    runs-on: ubuntu-latest
    needs: train
    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id:     ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region:            ${{ env.AWS_REGION }}

      - run: |
          aws ec2 run-instances \
            --image-id ami-XXXXXXXX \
            --instance-type t3.medium \
            --key-name my-keypair \
            --security-group-ids sg-XXXXXXXX \
            --iam-instance-profile Name=EC2-ECR-S3-Role \
            --user-data file://infra/ec2_launch.sh \
            --tag-specifications 'ResourceType=instance,TagSpecifications=[{Key=Name,Value=mnist-serve}]'
          echo "Serving instance launched."
```

---

### 6. Tests

#### `tests/test_train.py`

```python
import numpy as np
import sys

sys.path.insert(0, "train")
from train import build_cnn


def test_model_output_shape():
    """Model should output (batch_size, 10) for 10 digit classes."""
    model = build_cnn()
    dummy = np.zeros((4, 28, 28, 1))
    out = model.predict(dummy)
    assert out.shape == (4, 10), f"Expected (4, 10), got {out.shape}"


def test_model_output_is_probability():
    """Output should be a valid probability distribution (sums to 1)."""
    model = build_cnn()
    dummy = np.zeros((1, 28, 28, 1))
    out = model.predict(dummy)
    assert abs(out.sum() - 1.0) < 1e-5, "Output probabilities should sum to 1"
```

#### `tests/test_serve.py`

```python
from fastapi.testclient import TestClient
import numpy as np
from PIL import Image
import io
import sys
import unittest.mock as mock

# Mock boto3 and tensorflow so we don't need real S3 or a trained model in unit tests
with mock.patch("boto3.client"):
    with mock.patch("tensorflow.keras.models.load_model") as mock_load:
        mock_model = mock.MagicMock()
        mock_model.predict.return_value = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0]])
        mock_load.return_value = mock_model

        sys.path.insert(0, "serve")
        from app import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_predict_returns_digit():
    """POST an image and check that the response contains digit and confidence."""
    img = Image.new("L", (28, 28), color=255)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    res = client.post("/predict", files={"file": ("test.png", buf, "image/png")})
    assert res.status_code == 200
    assert "digit" in res.json()
    assert "confidence" in res.json()
```

---

### 7. Docker Compose (Local Dev Only)

Use this to run the full pipeline locally without AWS. Data flows through a shared Docker volume instead of S3.

#### `docker-compose.yml`

```yaml
version: "3.8"

volumes:
  shared_data:   # Shared volume — replaces S3 for local development

services:
  data:
    build: ./data
    volumes:
      - shared_data:/data
    # Override entrypoint to use local file saving instead of S3
    entrypoint: ["python", "-c", |
      import tensorflow as tf
      import numpy as np
      import os

      (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
      x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
      x_test  = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0

      os.makedirs('/data/processed', exist_ok=True)
      np.save('/data/processed/x_train.npy', x_train)
      np.save('/data/processed/y_train.npy', y_train)
      np.save('/data/processed/x_test.npy',  x_test)
      np.save('/data/processed/y_test.npy',  y_test)
      print('Local data prep done.')
    ]

  train:
    build: ./train
    volumes:
      - shared_data:/data
    depends_on:
      data:
        condition: service_completed_successfully
    # Override to use local paths instead of S3
    entrypoint: ["python", "-c", |
      import numpy as np
      import tensorflow as tf
      from tensorflow.keras import layers, models
      import json, os

      x_train = np.load('/data/processed/x_train.npy')
      y_train = np.load('/data/processed/y_train.npy')

      model = models.Sequential([
          layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
          layers.MaxPooling2D((2,2)),
          layers.Conv2D(64, (3,3), activation='relu'),
          layers.MaxPooling2D((2,2)),
          layers.Flatten(),
          layers.Dense(64, activation='relu'),
          layers.Dense(10, activation='softmax')
      ])
      model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
      history = model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.1)

      os.makedirs('/data/model', exist_ok=True)
      model.save('/data/model/cnn_mnist.keras')

      val_acc = history.history['val_accuracy'][-1]
      with open('/data/model/train_meta.json', 'w') as f:
          json.dump({'val_accuracy': val_acc}, f)
      print(f'Local training done. Val Accuracy: {val_acc:.4f}')

      if val_acc < 0.95:
          print('FAIL: Accuracy below threshold.')
          exit(1)
      print('PASS: Model approved.')
    ]

  serve:
    build: ./serve
    volumes:
      - shared_data:/data
    ports:
      - "8000:8000"
    depends_on:
      train:
        condition: service_completed_successfully
    # Override to load model from local volume instead of S3
    entrypoint: ["python", "-c", |
      import tensorflow as tf
      import numpy as np
      from fastapi import FastAPI, UploadFile
      from PIL import Image
      import io, uvicorn

      app = FastAPI()
      model = tf.keras.models.load_model('/data/model/cnn_mnist.keras')

      @app.get('/health')
      def health():
          return {'status': 'ok'}

      @app.post('/predict')
      async def predict(file: UploadFile):
          img = Image.open(io.BytesIO(await file.read())).convert('L').resize((28, 28))
          arr = np.array(img).reshape(1, 28, 28, 1).astype('float32') / 255.0
          pred = model.predict(arr)
          return {'digit': int(np.argmax(pred)), 'confidence': round(float(np.max(pred)), 4)}

      uvicorn.run(app, host='0.0.0.0', port=8000)
    ]
```

---

## Cost Breakdown

| Component | Instance Type | ~Hourly Cost | Usage Pattern |
|-----------|--------------|--------------|---------------|
| Training  | p3.2xlarge (GPU) | ~$3.00 | Runs for a few minutes, then terminates |
| Serving   | t3.medium (CPU)  | ~$0.04 | Runs continuously |

The GPU instance is the expensive one, but because it terminates immediately after training finishes, you only pay for the actual compute time (typically under a minute for MNIST). The serving instance stays up long-term but is cheap.

---

## Prerequisites

- **AWS Account** with the following:
  - An S3 bucket (update `S3_BUCKET` in all files)
  - An ECR repository (update `ECR_REGISTRY` in the workflow)
  - An IAM role (`EC2-ECR-S3-Role`) with permissions for ECR pull and S3 read/write, attached as an EC2 instance profile
  - A key pair for EC2 SSH access
  - A security group that allows inbound on port 8000
  - An AMI ID with Docker pre-installed (or use Amazon Linux 2)
- **GitHub Secrets** configured in your repository:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
- **Docker** installed locally (for local dev)
- **Python 3.11+** installed locally (for running tests)

---

## How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/your-username/mnist-cnn-pipeline.git
cd mnist-cnn-pipeline

# 2. Run tests
pip install tensorflow numpy fastapi httpx pillow pytest boto3
pytest tests/

# 3. Run the full pipeline locally via Docker Compose
docker compose up --build

# 4. Test the serving endpoint
curl -X POST http://localhost:8000/predict \
  -F "file=@path/to/your/digit_image.png"

# 5. Check health
curl http://localhost:8000/health
```
