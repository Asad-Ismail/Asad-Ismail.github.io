+++
draft = false
date = 2025-01-11T00:00:00Z
title = "ML Model Deployment on AWS: A Practical Guide"
description = "Hands-on guide to deploying ML models on AWS with real examples using SageMaker, Lambda, and Batch."
tags = ["Machine Learning", "MLOps", "Deployment", "AWS"]
categories = ["Machine Learning", "Engineering"]
authors = ["Asad Ismail"]
+++

# ML Model Deployment on AWS

Most ML projects should start with batch processing. It is cheaper, easier to debug, and forces you to think about whether you actually need real-time predictions. Only move to real-time endpoints when batch genuinely does not work for your use case.

This guide covers four deployment patterns with working AWS code.

## Four Deployment Patterns

Pick based on your latency and cost requirements:

| Pattern | Latency | Cost | AWS Service |
|---------|---------|------|-------------|
| Real-time API | <100ms | $$$ | SageMaker Endpoints |
| Batch | Hours | $ | SageMaker Batch Transform |
| Serverless | 100ms-5s | $$ | Lambda + API Gateway |
| Edge | <10ms | Free after deploy | IoT Greengrass |

---

## 1. Real-time API with SageMaker

**When to use:** User-facing applications that need instant responses. Fraud detection during checkout, content recommendations as users browse, or chatbot intent classification.

**Why SageMaker Endpoints:** Managed infrastructure with built-in load balancing, autoscaling, and A/B testing. No need to manage EC2 instances or containers yourself.

**Trade-offs:** Always-on instances cost money even when idle. For sporadic traffic, consider serverless instead.

**Example: Fraud detection API** that scores transactions in real-time during payment processing.

**Deploy a scikit-learn model:**

```python
import sagemaker
from sagemaker.sklearn import SKLearnModel

# Package your model
model = SKLearnModel(
    model_data='s3://my-bucket/models/fraud-detector.tar.gz',
    role='arn:aws:iam::123456789:role/SageMakerRole',
    entry_point='inference.py',
    framework_version='1.2-1'
)

# Deploy with autoscaling
predictor = model.deploy(
    initial_instance_count=2,
    instance_type='ml.m5.large',
    endpoint_name='fraud-detector-prod'
)

# Test it
result = predictor.predict([[0.5, 1.2, 0.8, 2.1]])
```

**Your inference.py:**

```python
import joblib
import numpy as np

def model_fn(model_dir):
    return joblib.load(f'{model_dir}/model.pkl')

def predict_fn(input_data, model):
    return model.predict_proba(input_data)[:, 1].tolist()
```

**Add autoscaling:**

```bash
aws application-autoscaling register-scalable-target \
  --service-namespace sagemaker \
  --resource-id endpoint/fraud-detector-prod/variant/AllTraffic \
  --scalable-dimension sagemaker:variant:DesiredInstanceCount \
  --min-capacity 1 --max-capacity 10

aws application-autoscaling put-scaling-policy \
  --policy-name fraud-scaling \
  --service-namespace sagemaker \
  --resource-id endpoint/fraud-detector-prod/variant/AllTraffic \
  --scalable-dimension sagemaker:variant:DesiredInstanceCount \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration \
    '{"TargetValue": 1000, "PredefinedMetricSpecification": {"PredefinedMetricType": "SageMakerVariantInvocationsPerInstance"}}'
```

**Cost:** ~$150/month for 2x ml.m5.large instances.

**Watch out for:** Endpoint updates take 5-10 minutes and cause brief downtime unless you use blue-green deployments. Test your autoscaling before you need it - scaling from 2 to 10 instances takes several minutes, not seconds.

---

## 2. Batch Processing with SageMaker Batch Transform

**When to use:** Predictions that can wait hours. Nightly churn scoring, weekly lead prioritization, or pre-computing recommendations for all users.

**Why Batch Transform:** Spins up instances only during the job, then shuts down. Pay for 20 minutes of compute instead of 24/7 endpoint costs.

**Trade-offs:** Results are stale by the time you use them. Not suitable for real-time decisions.

**Example: Churn prediction** that runs every night at 2 AM, scores all customers, and writes results to S3 for the marketing team.

```python
from sagemaker.sklearn import SKLearnModel

model = SKLearnModel(
    model_data='s3://my-bucket/models/churn-model.tar.gz',
    role='arn:aws:iam::123456789:role/SageMakerRole',
    entry_point='inference.py',
    framework_version='1.2-1'
)

# Run batch transform
transformer = model.transformer(
    instance_count=4,
    instance_type='ml.m5.xlarge',
    output_path='s3://my-bucket/predictions/2025-01-27/'
)

transformer.transform(
    data='s3://my-bucket/data/customers.csv',
    content_type='text/csv',
    split_type='Line'
)

transformer.wait()  # Takes ~20 mins for 1M rows
```

**Schedule with EventBridge:**

```json
{
  "schedule": "cron(0 2 * * ? *)",
  "targets": [{
    "arn": "arn:aws:sagemaker:us-east-1:123456789:pipeline/daily-scoring",
    "roleArn": "arn:aws:iam::123456789:role/EventBridgeSageMaker"
  }]
}
```

**Cost:** ~$5 for scoring 1M records (4x ml.m5.xlarge for 20 mins).

**Tip:** Store predictions with timestamps and model versions. When you retrain, you will want to compare old vs new predictions on the same data. Without versioning, you cannot debug why results changed.

---

## 3. Serverless with Lambda

**When to use:** Low or unpredictable traffic. Internal tools, MVPs, or event-driven workflows where a file upload triggers prediction.

**Why Lambda:** Zero cost when idle. Scales automatically from 0 to thousands of concurrent requests.

**Trade-offs:** Cold starts add 3-5 seconds latency. Model size limited to 250MB (deployment package) or 10GB (container image). Max 15 minute timeout.

**Example: Document classifier** that triggers when PDFs are uploaded to S3, classifies them, and routes to the right department.

**Lambda function:**

```python
import json
import boto3
import pickle
import os

# Load model at cold start
s3 = boto3.client('s3')
s3.download_file('my-bucket', 'models/model.pkl', '/tmp/model.pkl')
model = pickle.load(open('/tmp/model.pkl', 'rb'))

def lambda_handler(event, context):
    body = json.loads(event['body'])
    features = body['features']
    
    prediction = model.predict([features])[0]
    proba = model.predict_proba([features])[0].max()
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'prediction': int(prediction),
            'confidence': float(proba)
        })
    }
```

**Deploy with AWS SAM** (Serverless Application Model - a CLI tool that packages and deploys Lambda functions):

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  PredictFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.lambda_handler
      Runtime: python3.11
      MemorySize: 512
      Timeout: 30
      Events:
        Predict:
          Type: Api
          Properties:
            Path: /predict
            Method: post
```

**Cold starts:** The first request after idle time takes 3-5 seconds. Provisioned concurrency keeps instances warm:

```bash
aws lambda put-provisioned-concurrency-config \
  --function-name PredictFunction \
  --qualifier prod \
  --provisioned-concurrent-executions 5
```

**Cost:** ~$0.20 per 1000 requests + $3.50/month per provisioned instance.

**Honest take:** Lambda works great for small models under 50MB. Once you start fighting package size limits, switching to container images, or paying for provisioned concurrency to avoid cold starts, you have probably outgrown Lambda. Just use SageMaker at that point.

---

## 4. Edge with IoT Greengrass

**When to use:** Devices with unreliable connectivity, strict latency requirements, or data privacy constraints that prevent sending data to the cloud.

**Why Greengrass:** Runs inference locally on the device. Works offline. Sub-10ms latency since there is no network round-trip.

**Trade-offs:** Limited compute on edge devices. Models must be small (typically under 100MB). Harder to update and monitor than cloud deployments.

**Common devices:** Raspberry Pi, NVIDIA Jetson, industrial gateways, cameras with onboard compute.

**Example: Quality inspection** on a factory floor camera that detects defects in real-time without sending images to the cloud.

**Step 1: Convert model to ONNX** (smaller and runs on CPU without framework dependencies):

```python
# Convert to ONNX for edge
import torch

model = torch.load('model.pt')
dummy = torch.randn(1, 10)

torch.onnx.export(
    model, dummy, 'model.onnx',
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={'input': {0: 'batch'}}
)
```

**Step 2: Create Greengrass component** (recipe.yaml):

```yaml
ComponentName: ml-inference
ComponentVersion: 1.0.0
ComponentConfiguration:
  DefaultConfiguration:
    ModelPath: /greengrass/v2/models/model.onnx
Manifests:
  - Platform:
      os: linux
    Artifacts:
      - URI: s3://my-bucket/components/inference.zip
    Lifecycle:
      Run: python3 {artifacts:path}/inference.py
```

**Step 3: Run inference on device:**

```python
import onnxruntime as rt
import numpy as np

session = rt.InferenceSession('/greengrass/v2/models/model.onnx')

def predict(features):
    input_name = session.get_inputs()[0].name
    return session.run(None, {input_name: np.array([features], dtype=np.float32)})[0]
```

**Honest take:** Edge deployment is harder than it looks. Debugging a model running on a device in a factory is painful compared to checking CloudWatch logs. Start with cloud deployment and only go edge when you have a clear reason (latency, connectivity, privacy). The operational overhead is significant.

---

## Monitoring

Models degrade silently. The data distribution shifts, upstream systems change, or bugs creep into feature pipelines. Without monitoring, you only find out when users complain.

**Start simple:** Most teams set up elaborate drift detection but forget basic latency alerts. Get latency and error rate alarms working first. Add drift detection later.

**Three things to monitor:**

1. **Infrastructure:** Latency, error rates, CPU/memory usage
2. **Data quality:** Input distribution drift from training data
3. **Model performance:** Prediction accuracy over time (requires delayed labels)

**Latency and error alarms** (alert before users notice):

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# Latency alarm
cloudwatch.put_metric_alarm(
    AlarmName='HighLatency-FraudDetector',
    MetricName='ModelLatency',
    Namespace='AWS/SageMaker',
    Dimensions=[{'Name': 'EndpointName', 'Value': 'fraud-detector-prod'}],
    Statistic='p99',
    Period=300,
    EvaluationPeriods=2,
    Threshold=500,  # 500ms
    ComparisonOperator='GreaterThanThreshold',
    AlarmActions=['arn:aws:sns:us-east-1:123456789:alerts']
)

# Error rate alarm  
cloudwatch.put_metric_alarm(
    AlarmName='HighErrors-FraudDetector',
    MetricName='Invocation5XXErrors',
    Namespace='AWS/SageMaker',
    Dimensions=[{'Name': 'EndpointName', 'Value': 'fraud-detector-prod'}],
    Statistic='Sum',
    Period=300,
    EvaluationPeriods=1,
    Threshold=10,
    ComparisonOperator='GreaterThanThreshold',
    AlarmActions=['arn:aws:sns:us-east-1:123456789:alerts']
)
```

**Data drift detection with SageMaker Model Monitor:**

```python
from sagemaker.model_monitor import DefaultModelMonitor

monitor = DefaultModelMonitor(
    role='arn:aws:iam::123456789:role/SageMakerRole',
    instance_count=1,
    instance_type='ml.m5.large'
)

# Create baseline from training data
monitor.suggest_baseline(
    baseline_dataset='s3://my-bucket/data/training.csv',
    dataset_format={'csv': {'header': True}}
)

# Schedule hourly checks
monitor.create_monitoring_schedule(
    monitor_schedule_name='fraud-drift-monitor',
    endpoint_input='fraud-detector-prod',
    output_s3_uri='s3://my-bucket/monitoring/',
    schedule_cron_expression='cron(0 * * * ? *)'
)
```

**Reality check:** Drift detection tells you something changed, not whether it matters. A feature distribution can shift without affecting model accuracy. Do not auto-retrain based on drift alone - investigate first.

---

## Rollback Strategy

New models fail in production. Maybe the training data had a bug, or the model overfits to recent patterns. You need to revert to the previous version in seconds, not hours.

**SageMaker production variants** let you run multiple model versions behind the same endpoint. Route 10% of traffic to the new model, watch metrics, then gradually shift traffic or rollback instantly.

**Example: Canary deployment** with 10% traffic to new model:

```python
from sagemaker import ModelPackage

# Deploy new model to 10% traffic
predictor.update_endpoint(
    initial_instance_count=2,
    instance_type='ml.m5.large',
    model_name='fraud-detector-v2',
    variant_name='v2',
    initial_variant_weight=0.1  # 10% traffic
)

# Metrics stable after 1 hour? Shift all traffic
sm = boto3.client('sagemaker')
sm.update_endpoint_weights_and_capacities(
    EndpointName='fraud-detector-prod',
    DesiredWeightsAndCapacities=[
        {'VariantName': 'v1', 'DesiredWeight': 0},
        {'VariantName': 'v2', 'DesiredWeight': 1}
    ]
)

# If something breaks, instant rollback
sm.update_endpoint_weights_and_capacities(
    EndpointName='fraud-detector-prod',
    DesiredWeightsAndCapacities=[
        {'VariantName': 'v1', 'DesiredWeight': 1},
        {'VariantName': 'v2', 'DesiredWeight': 0}
    ]
)
```

---

## Cost Comparison

ML infrastructure costs can spiral. A real-time endpoint running 24/7 costs 30x more than a batch job that runs for 20 minutes. Choose the cheapest option that meets your latency requirements.

| Scenario | Service | Monthly Cost |
|----------|---------|--------------|
| 1M predictions/day, real-time | SageMaker (2x ml.m5.large) | ~$150 |
| 1M predictions/day, batch | Batch Transform | ~$5 |
| 10K predictions/day, serverless | Lambda | ~$2 |
| Edge inference | Greengrass | ~$0 (device cost only) |

If you can wait 6 hours for results, batch costs 30x less than real-time.

---

## TL;DR

Start with batch. Move to real-time only when you must. Skip edge unless you have a clear reason.

Set up latency alerts before anything else. Add Model Monitor after your basic monitoring works.
