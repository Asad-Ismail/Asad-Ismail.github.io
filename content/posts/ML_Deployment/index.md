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


I will now go over throw show the code for Sagemaker Batch Transform, Real Time endpoints and Async Endpoints with the example of Instance segmentation using Detectron2 MaskRCNN implementation. Why instance segemntation example? I believe it is not covered as much as object detection and classification when it has the most utility in industry for computer vision tasks as it combine object detection with segmentation giving the class information along with precise object boundary for measurements. I will train the model using detectron2 example. Train it on sample dataset provided in detectron2 repo, the focus is not on the training but deployment but for the sake of completeness I will go over through complete example.

## Instance Segmenation Training and inference Locally

An example of basic training and inference of detectron2 maskrcnn model is given in this repo https://github.com/facebookresearch/detectron2?tab=readme-ov-file

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

see full example here https://colab.research.google.com/drive/16jcaJoc6bCFAQ96jDe2HwtXj7BMD_-m5#scrollTo=U5LhISJqWXgM


Once we have trained, evaluated and tested the model we want to deploy the model. We will show the most general case of deployment to build our own custom container so it is aplicable to pretty much all ML models not tied down to specific container proided by sagemaker.

## AWS Batch Transform


























