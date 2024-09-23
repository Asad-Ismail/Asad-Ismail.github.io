+++
draft = false
date = 2024-09-14T00:00:00+02:00
title = "Efficient Deep Learning Part 1"
description = "Exploring techniques to make deep learning models more efficient"
slug = ""
authors = []
tags = ["Deep Learning", "Efficiency", "Model Optimization"]
categories = ["Machine Learning"]
externalLink = ""
series = ["Efficient Deep Learning"]
+++

# Efficient Deep Learning Part 1

Deep learning models have revolutionized many fields, from computer vision to natural language processing. However, they often come with a significant drawback: computational inefficiency. Large models require substantial computational resources, which can lead to high costs and slow inference times. In this series, we'll explore various techniques to make deep learning models more efficient without significantly compromising performance.

## Why Efficiency Matters

- **Resource Constraints**: Not all environments have access to high-performance computing resources. Deploying models on edge devices like smartphones or IoT devices requires efficient models.
- **Cost Reduction**: Efficient models reduce the computational resources needed, lowering operational costs.
- **Environmental Impact**: Reducing computational demands also decreases energy consumption, contributing to greener AI practices.

In this post we will focus more on Basics of DL layers. Note most of the below content is distilled version of [MIT efficient DL](https://hanlab.mit.edu/courses/2024-fall-65940) course which I highly recommend if you want to have a deeper dive

## Basics of Deep Learning Layers

### Linear Layers

Outputs are connected to all inputs resulting normally in too many paramerets.

Inputs: n,ci
Outputs: n,co
weights: (co,ci)
Bias: (co)

### Convolution Layer
2D convlotion. Output is connected to input thorugh only receptive field (kernel size). 

Inputs: (n,ci,hi,wi)
Outputs: (n,co,ho,wo)
Weights: (ci,co,kh,kw)
bias: (co)
Normally padding is applied to input to keep the original input size as the outout size is given by

so=(si+2p-Kh/s)+1

Each successive convolutions add k-1 to the receptive field size, with L layers the receptive field size **Lx(K-1)+1**
