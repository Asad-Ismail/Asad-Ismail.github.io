+++ 
draft = false
date = 2024-08-16T00:36:50+02:00
title = "Machine Learning Model deployment"
description = "Machine learning deployment"
slug = ""
authors = []
tags = []
categories = []
externalLink = ""
series = []
+++


## Machine Learning Model Deployment

After successfully building your ML/DL model in a notebook, the next critical step is deployment—getting your model out into the world to serve customers. There are two primary avenues for deploying machine learning models:

1. **Edge Deployment**
2. **Cloud Deployment**

### Edge Deployment

Edge deployment involves placing the model directly on the device where it will be used. This approach is particularly valuable in situations where:

1. **Latency Requirements**: Real-time deployment and control are essential, and network latency is unacceptably high.
2. **No Network Availability**: The model must operate in environments without internet connectivity.

#### Examples:
- Deploying perception models for advanced driving assistance systems (ADAS) or self-driving cars, where split-second decisions are critical.
- Deploying ML models on machinery in remote fields with no internet connectivity, where immediate, on-the-spot results are required.

### Cloud Deployment

Cloud deployment allows you to leverage the power and flexibility of cloud computing. This can be done in two main ways:

1. **Self-Managed Cloud Deployments**: Using tools like KFServing or KServe, organizations can deploy and manage ML models in the cloud on their own. This option provides extensive control but comes with a learning curve, making it more suitable for larger companies with the necessary resources.

2. **Managed Cloud Services**: Alternatively, you can opt for managed services from major cloud providers like AWS, Azure, and Google Cloud Platform (GCP). These services simplify deployment and management, though they may have certain limitations.

Below is a visual representation of the market share among major cloud providers for ML model deployment. The data is from 2022, and it's possible that Azure, with its partnership with OpenAI, has already surpassed AWS.


![Major cloud providers usage 2022](/images/cloud_providers.png){.custom-size}
>



### Focus on AWS for ML Deployment

For this discussion, we will focus on deploying models using AWS, though Azure and GCP offer similar services. Here are the key types of ML deployments available on AWS:

#### AWS Batch

- **Convert the model to Docker file**: Run this Docker container by events or scheduled tasks.

#### SageMaker Batch Processing

- **Payload Size**: Max 100 MB mini-batch payload size.
- **Higher Throughput**: Suitable for large batch processing.
- **Event-Triggered**: Triggered via S3 events, for example.

#### Real-Time Endpoints

**Pros:**
- **Low Latency**: Ideal for scenarios where immediate responses are crucial.
- **API Integration**: Invoke the endpoint with your data (e.g., JSON input) via HTTP requests, receiving predictions almost instantly.
- **Auto-Scaling**: AWS automatically scales the endpoint based on demand.
- **Flexible Options**: Support for both CPU and GPU instances.

**Cons:**
- **Payload Size Limit**: The maximum allowed payload is 6MB, which can be restrictive for high-resolution images, necessitating downscaling or compression.
- **Timeout Limit**: The model must return results within 60 seconds, which may be limiting for complex computations.

#### Async Endpoints

**Pros:**
- **Queue Inputs**: Queue inputs for processing later.
- **API Integration**: Similar to real-time endpoints but with different operational characteristics.
- **Auto-Scaling**: AWS automatically scales the endpoint based on demand.
- **Flexible Options**: Support for both CPU and GPU instances.
- **Larger Payload Size**: Supports up to 1GB payload size.
- **Longer Timeout**: Allows up to 15 minutes of processing time.

**Cons:**
- **Near Real-Time**: Offers near real-time performance, but not as immediate as real-time endpoints.








