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


{{< customimage src="/images/cloud_providers.png" alt="Cloud Market Share" caption="Cloud Market share @2022" width="50%" >}}


### Focus on AWS for ML Deployment

In this discussion, we'll focus on deploying machine learning models using AWS, although Azure and GCP offer similar services. Below are the key types of ML deployments available on AWS.


#### AWS Batch Processing

AWS Batch is a versatile batch processing service that enables you to run large-scale computing workloads on AWS.

**Advantages:**
- **Versatility:** Suitable for a wide range of batch jobs, beyond just machine learning.
- **Custom Docker Containers:** Supports running jobs within custom Docker images, offering flexibility in the environment setup.
- **Broad Use Cases:** Applicable for tasks like data processing, image rendering, and large-scale simulations.

**Disadvantages:**
- **General-Purpose Nature:** Not specifically optimized for machine learning tasks, which might require additional setup or configuration.
- **Potentially Complex Configuration:** Depending on the use case, configuring batch jobs might require more detailed setup compared to services tailored to specific tasks like ML.

#### SageMaker Batch Transform

SageMaker Batch Transform is designed specifically for batch inference tasks in machine learning.

**Advantages:**
- **ML-Specific:** Optimized for batch processing of machine learning model inferences, ensuring a streamlined workflow.
- **Seamless Integration:** Easily integrates with other SageMaker services like training and deployment, simplifying the end-to-end ML process.
- **High Throughput:** Designed for large-scale ML tasks, allowing for efficient processing of extensive datasets.
- **Event-Driven:** Can be triggered by S3 events, enabling automated processing of new data as it arrives.

**Disadvantages:**
- **Limited to ML Use Cases:** Not suitable for non-ML batch processing tasks, which limits its flexibility compared to AWS Batch.
- **Dependent on SageMaker Ecosystem:** While integration is an advantage, it also means that it's less flexible if you need to use non-SageMaker services.

### Real-Time Endpoints

Real-Time Endpoints in SageMaker are used for scenarios where immediate inference is required. They provide a scalable and low-latency way to get predictions as soon as data is sent to the model.

**Advantages:**
- **Low Latency:** Delivers immediate responses, making it ideal for real-time applications.
- **API Integration:** Can be easily invoked via HTTP requests, making it straightforward to integrate into existing applications.
- **Auto-Scaling:** Automatically adjusts the number of instances based on demand, ensuring performance consistency.
- **Flexible Instance Options:** Offers both CPU and GPU instances, catering to different performance needs.

**Disadvantages:**
- **Payload Size Limit:** The maximum input size is 6 MB, which might require you to downscale or compress larger inputs.
- **Timeout Constraints:** The model needs to return results within 60 seconds, which can be limiting for more complex models.

### Asynchronous Endpoints

Asynchronous Endpoints are designed for scenarios where inference does not need to be instantaneous. They allow for processing larger payloads and longer processing times, making them suitable for more complex or batch-like tasks.

**Advantages:**
- **Handles Larger Payloads:** Supports input sizes up to 1 GB, which is significantly higher than real-time endpoints.
- **Extended Processing Time:** Allows up to 15 minutes for inference, accommodating more complex computations.
- **Queue Inputs:** Inputs can be queued, which is useful for handling large volumes of data that do not require immediate processing.
- **Auto-Scaling:** Automatically scales based on demand, similar to real-time endpoints.

**Disadvantages:**
- **Near Real-Time Performance:** While it supports larger payloads and longer processing times, the latency is higher compared to real-time endpoints.
- **More Complex Workflow:** Managing asynchronous jobs might require more careful monitoring and management compared to the simpler real-time endpoint approach.


### Sagemaker Serverless Inference

Serverless Inference enables to deploy and scale ML models without configuring or managing any of the underlying infrastructure. We can use serveless inference for cpu only loads for requests where there is idle time between requests.

**Advantages:**
- **Autoscaling:** Serverless Inference scales your endpoint down to 0, helping you to minimize your costs.

**Disadvantages:**
- **CPU inference:** Currently it supports only cpu compute.
- **Cold start:** We have to tolerate cold start for intial requests.


More details here https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html


I will now go through and show the code for SageMaker Batch Transform, Real-Time Endpoints, and Async Endpoints with the example of instance segmentation using Detectron2's Mask R-CNN implementation. Why an instance segmentation example? I believe it is not covered as much as object detection and classification, even though it has the most utility in the industry for computer vision tasks, as it combines object detection with segmentation, giving the class information along with precise object boundaries for measurements. I will train the model using a Detectron2 example, and train it on a sample dataset provided in the Detectron2 repo. The focus is not on the training but deployment, but for the sake of completeness, I will go through the complete example.

## Instance Segmentation Training and inference Locally

An example of basic training and inference of detectron2 maskrcnn model is given in this repo [Detectron2](https://github.com/facebookresearch/detectron2?tab=readme-ov-file)

A simple example of training maskrcnn model 
```python
from detectron2.config import get_cfg
cfg = get_cfg()
model_arch="COCO-InstanceSegmentation/mask_rcnn_R_101_C4_3x.yaml"
cfg.merge_from_file(model_zoo.get_config_file(model_arch))
trainer = DefaultTrainer(cfg) 
trainer.resume_or_load(resume=False)
trainer.train()
```


and we can use this model to perorm inference like below

```python
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
cfg = get_cfg()
model_arch="COCO-InstanceSegmentation/mask_rcnn_R_101_C4_3x.yaml"
cfg.merge_from_file(model_zoo.get_config_file(model_arch))
cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")  # path to the model we just trained
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set a custom testing threshold
predictor = DefaultPredictor(cfg)
im = cv2.imread(d["file_name"])
outputs = predictor(im)
```

see full example here [Detectron2 Example](https://colab.research.google.com/drive/16jcaJoc6bCFAQ96jDe2HwtXj7BMD_-m5#scrollTo=U5LhISJqWXgM)

Once we have trained, evaluated, and tested the model, we want to deploy it. We will show the most general case of deployment by building our own custom container so it is applicable to pretty much all ML models, not tied down to specific containers provided by SageMaker. The complete code can be found in the [Repo](https://github.com/Asad-Ismail/ml-model-deployment)

## Build Custom Container

Before deploying our models to any of the deployment strategies, we need to first dockerize our model. Below is the Dockerfile for Async and Real-Time Endpoints:

``` bash
FROM nvcr.io/nvidia/pytorch:23.12-py3 as build

RUN apt update && DEBIAN_FRONTEND="noninteractive" apt -y install tzdata && \
    apt install -y zip libgl1-mesa-glx netbase libopencv-dev libopenblas-dev nginx && \
    apt clean && rm -rf /var/lib/apt/lists/*

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py && \
    python -m pip install pip==24.2 --no-cache-dir

COPY ./scripts /opt/program

# Set work directory and install Python dependencies
WORKDIR /opt/program
## specific torch and torchvision version
RUN pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 --extra-index-url https://download.pytorch.org/whl/cu113 --no-cache-dir

RUN pip install -r requirements.txt --no-cache-dir

# Set environment variables
ENV PYTHONUNBUFFERED=TRUE \
    PYTHONDONTWRITEBYTECODE=TRUE \
    PATH="/opt/program:${PATH}"

RUN chmod +x /opt/program/serve

```

To build docker and push to ECR

``` bash
docker build -t $image_tag -f $dockerfile .
docker tag $image_tag $account.dkr.ecr.$region.amazonaws.com/$repo_name:latest
docker push $account.dkr.ecr.$region.amazonaws.com/$repo_name:latest

```

It essentially gets the base NVIDIA image from NGC and installs dependencies for running Detectron2.

## Registering the Model

To properly arrange and register the models and have proper metadata assigned to them, it is better to arrange models in Model Groups. We can also skip this step and go directly to the next step, but I highly recommend it. The model at this point is defined by two things: a model container, which was pushed to ECR in the last step, and a gzipped model file, which contains the model config file and model weights. Using both, we can deploy the model in SageMaker.

```python

model_package_group_name = "name-of-model-group"
model_package_group_input_dict = {
 "ModelPackageGroupName" : model_package_group_name,
 "ModelPackageGroupDescription" : "Test Sample model package group"
}
create_model_package_group_response = sm_client.create_model_package_group(**model_package_group_input_dict)

modelpackage_inference_specification =  {
    "InferenceSpecification": {
      "Containers": [
         {
            "Image": image_uri,
            "ModelDataUrl": model_url
         }
      ],
      "SupportedContentTypes": [ "json" ],
      "SupportedResponseMIMETypes": [ "json/csv" ],
   }
 }

 create_model_package_input_dict = {
    "ModelPackageGroupName" : model_package_group_name,
    "ModelPackageDescription" : "Model to do something x",
    "ModelApprovalStatus" : "PendingManualApproval"
}
create_model_package_input_dict.update(modelpackage_inference_specification)
create_model_package_response = sm_client.create_model_package(**create_model_package_input_dict)
model_package_arn = create_model_package_response["ModelPackageArn"]

```


## Real Time endpoints

To deploy our model as a real-time endpoint using SageMaker, we can use the ModelPackage class to create a model from our registered model package and then deploy it to an endpoint. This setup allows you to serve predictions in real time with minimal latency, which is ideal for applications requiring immediate responses.

```python

# Create a SageMaker session and create model group
sagemaker_session = sagemaker.Session()
model_package_arn="arn:aws:sagemaker:xxxx"

model = ModelPackage(role=role, 
                     model_package_arn=model_package_arn, 
                     sagemaker_session=sagemaker_session)

async_config = AsyncInferenceConfig(
    output_path='s3://your-bucket/async_output/',
    max_concurrent_invocations_per_instance=1
)

# Deploy the model to an endpoint
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.p3.2xlarge",
    endpoint_name="your-endpoint-name"
)

# Perform real-time inference
test_image = open("test_image.jpg", "rb").read()
response = predictor.predict(test_image)

```


## Async Inference

For scenarios where immediate responses are not critical and you need to handle large payloads or longer processing times, you can deploy your model using SageMaker's Asynchronous Inference. This method allows your endpoint to process requests asynchronously, making it suitable for batch processing or complex computations.

```python

# Create a SageMaker session and specify your role
sagemaker_session = sagemaker.Session()
model_package_arn="arn:aws:sagemaker:xxxx"

model = ModelPackage(role=role, 
                     model_package_arn=model_package_arn, 
                     sagemaker_session=sagemaker_session)

async_config = AsyncInferenceConfig(
    output_path='s3://your-bucket/async_output/',
    max_concurrent_invocations_per_instance=1
)

# Deploy model as endpoint
predictor = model.deploy(
    initial_instance_count=1,
    instance_type='ml.p3.2xlarge',
    endpoint_name=endpoint_name,
    async_inference_config=async_config
)

waiter = sm_client.get_waiter("endpoint_in_service")
print("Waiting for endpoint to create...")
waiter.wait(EndpointName=endpoint_name)
resp = sm_client.describe_endpoint(EndpointName=endpoint_name)

```


### Attaching Autoscaling to endpoint

If we expect irregular requests, to save cost and be responsive, it is best to attach autoscaling to the endpoints so it can scale out if we get a lot of traffic requests and scale in if there are not many requests. We can have different metrics to monitor to scale out and in; here we are using SageMakerVariantInvocationsPerInstance.

```python

client = boto3.client("application-autoscaling") 

## Using autoscaling for all trafic and the current endpoint
resource_id = ("endpoint/" + endpoint_name + "/variant/" + "AllTraffic")  

# Configure Autoscaling on asynchronous endpoint down to zero instances
response = client.register_scalable_target(
    ServiceNamespace="sagemaker",
    ResourceId=resource_id,
    ScalableDimension="sagemaker:variant:DesiredInstanceCount",
    MinCapacity=0,
    MaxCapacity=1,
)

response = client.put_scaling_policy(
    PolicyName="Invocations-ScalingPolicy",
    ServiceNamespace="sagemaker",  # The namespace of the AWS service that provides the resource.
    ResourceId=resource_id,  # Endpoint name
    ScalableDimension="sagemaker:variant:DesiredInstanceCount",  # SageMaker supports only Instance Count
    PolicyType="TargetTrackingScaling",  # 'StepScaling'|'TargetTrackingScaling'
    TargetTrackingScalingPolicyConfiguration={
        "TargetValue": 1.0,  # The target value for the metric. - here the metric is - SageMakerVariantInvocationsPerInstance
        "PredefinedMetricSpecification": {
            "PredefinedMetricType": "SageMakerVariantInvocationsPerInstance"
        },
        "ScaleInCooldown": 2,  # The cooldown period helps you prevent your Auto Scaling group from launching or terminating
        # additional instances before the effects of previous activities are visible.
        # You can configure the length of time based on your instance startup time or other application needs.
        # ScaleInCooldown - The amount of time, in seconds, after a scale in activity completes before another scale in activity can start.
        "ScaleOutCooldown": 2,  # ScaleOutCooldown - The amount of time, in seconds, after a scale out activity completes before another scale out activity can start.
        # 'DisableScaleIn': True|False - ndicates whether scale in by the target tracking policy is disabled.
        # If the value is true , scale in is disabled and the target tracking policy won't remove capacity from the scalable resource.
        "DisableScaleIn": False 
    },
)

```

### AWS Sagemaker Batch Transform 

1. For SageMaker Batch Transform, the Dockerfile is slightly different; see details here: [Doclerfile_BT](https://github.com/Asad-Ismail/ml-model-deployment/blob/main/sm_batch_transform/Dockerfile)

2. Building and registering the model steps stay the same; also given here: [Build&Register](https://github.com/Asad-Ismail/ml-model-deployment/blob/main/sm_batch_transform/Dockerfile)

3. Create SageMaker Batch Transform job:

```python

sm_cli = sagemaker_session.sagemaker_client

transformer=model.transformer(instance_count=1, instance_type="ml.p3.2xlarge", output_path=model_outputs_path,max_payload=100)

transformer.transform(
    data='s3://path_to_your_images/input/', 
    data_type="S3Prefix",
    content_type="application/x-image",
    wait=True
)

job_info = sm_cli.describe_transform_job(TransformJobName=transformer.latest_transform_job.name)

```

## Additional Comments and Conclusion

We have explored various strategies for deploying machine learning models, focusing on AWS services like SageMaker for real-time endpoints, asynchronous inference, and batch transform jobs. By using a practical example of instance segmentation with Detectron2's Mask R-CNN, We have demostrated following poiints:

- Flexibility: Custom containers allow you to deploy a wide range of models, not limited to specific frameworks.
- Scalability: AWS services like SageMaker provide robust scaling options to handle varying workloads.
- Performance: Options like real-time endpoints ensure low-latency responses for time-sensitive applications.
Limitations and Considerations:

We did not consider and some topics for future are:

- Deployment Strategies: In real-world scenarios, you'd often want to gradually shift traffic to new endpoints to minimize risks. Techniques like canary deployments and A/B testing allow you to test new models on a small percentage of traffic before full rollout.

- Continuous Integration/Continuous Deployment (CI/CD): Automate your deployment pipeline for efficient updates and scaling.
Advanced Deployment Strategies: Explore canary deployments, blue/green deployments, and A/B testing to improve deployment safety and effectiveness.
By understanding these deployment strategies and their strengths and limitations, you can make informed decisions on how best to serve your machine learning models to meet your application's needs.

Feel free to reach out or consult the [Repo](https://github.com/Asad-Ismail/ml-model-deployment/blob/main/sm_batch_transform/batch_transform.ipynb) for the complete code.



### References

**AWS SageMaker Documentation:**

- [Real-Time Inference](https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html)
- [Asynchronous Inference](https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html)
- [Batch Transform](https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html)
- [Serverless Inference](https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html)

**Detectron2 Resources:**

- [Detectron2 GitHub Repository](https://github.com/facebookresearch/detectron2)
- [Detectron2 Documentation](https://detectron2.readthedocs.io/)

**AWS Autoscaling:**

- [Application Auto Scaling Documentation](https://docs.aws.amazon.com/autoscaling/application/userguide/what-is-application-auto-scaling.html)
- [Scaling SageMaker Endpoints](https://docs.aws.amazon.com/sagemaker/latest/dg/inference-endpoints-auto-scaling.html)

**Advanced Deployment Strategies:**

- [Canary Deployments with AWS SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/deployment-guardrails-blue-green-canary.html)
- [Blue/Green Deployments](https://docs.aws.amazon.com/sagemaker/latest/dg/deployment-guardrails-blue-green.html)