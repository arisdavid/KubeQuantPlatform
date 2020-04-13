## Risk Quant Model Platform

## Introduction
Risk Quant Model Platform (RQMP) is an experimental model execution platform. 
The platform is responsible for orchestrating containerised financial models inside the cluster. 
At present, it's configured to orchestrate a model as a job on a single ephemeral pod. 

## Kubernetes Local Development
For local development and testing setup a Kubernetes cluster using minikube. 

https://kubernetes.io/docs/setup/learning-environment/minikube/

Launch a minikube cluster using the following command:
```
minikube start 
```

Create a namespace
```
kubectl create namespace <namespace_name>
```

Set the namespace context
```
kubectl config set-context $(kubectl config current-context) --namespace=<namespace_name>
```

Ensure you're inside the Kubernetes environment as this is where the images will be built
 
```
eval $(minikube docker-env)
```

## Optional 
For interacting with the cluster it would be handy to have k9s installed - https://github.com/derailed/k9s. 
It's an interactive UI tool for interacting with Kubernetes cluster.


## Helm 
Helm is a tool for managing Kubernetes charts. Charts are packages of pre-configured Kubernetes resources. To install Helm, refer to the Helm install guide and ensure that the helm binary is in the PATH of your shell.

## Build docker images

There are two sample models that can be executed on the platform - Geometric Brownian Motion and KMV.

Clone the the following repositories and build the corresponding Docker images inside the Kubernetes cluster (minikube cluster)

- https://github.com/arisdavid/rqmp-credit-risk-models
```
docker build -t credit-models:latest .
```

- https://github.com/arisdavid/rqmp-market-risk-models
```
docker build -t market-risk-models:latest .
```

Task Queue Manager (this repository)
```
docker build -t task-queue-manager:latest .
```

## Scenario 1: Local execution

Execute the command below from the RiskQuantModelPlatform root directory.

#### KMV Model
```
python3 main.py kmv 1000000 900000 500000 0.18 0.12
```

#### Monte Carlo Simulation of GBM Model

```
python3 main.py mcs gbm 1000 200 0.2 0.18 365 250
```



## Scenario 2: AWS S3 File Upload

Spin up AWS Resources using Terraform
```
terraform apply
```

To Install
```
helm install --namespace=rqmp tqm-chart ./tqm-chart --values ./tqm-chart/values.dev.yaml
```

To uninstall
```
helm uninstall --namespace=rqmp tqm-chart ./tqm-chart
```

Drop a file into one of the s3 buckets e.g. ```aws s3 cp <file> s3://bucket-name```

## Screenshots
#### 1. Local Execution
![![Image of K9s]](https://i.imgur.com/0vp4nBV.gif)
