## Risk Quant Model Platform

### Introduction
Risk Quant Model Platform (RQMP) is an experimental model execution platform. 
The platform is responsible for orchestrating containerised financial models inside the cluster. 
At present, it's configured to run execute a model on a single ephemeral pod. 

### Kubernetes Local Development
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

Optional: for interacting with the cluster it would be handy to have k9s installed - https://github.com/derailed/k9s. It's an interactive UI tool for interacting with Kubernetes cluster.

### Setup

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

### How to orchestrate the sample models

Execute the command below from the RiskQuantModelPlatform root directory.

#### KMV Model
```
python3 main.py kmv 1000000 900000 500000 0.18 0.12
```

#### Monte Carlo Simulation of GBM Model
```
python3 main.py mcs gbm 1000 200 0.2 0.18 365 250
```

#### Current Models
| Arg | Model Name                | Model Category | Usage                              |
|-----|---------------------------|----------------|------------------------------------|
| gbm | Geometric Brownian Motion | Market Risk    | Forecasting equity prices          |
| kmv | KMV Merton Model          | Credit Risk    | Forecasting Probability of Default |
| mcs | Monte Carlo Simulation    | N/A            | Repeated random sampling           |


## Screenshots
![![Image of K9s]](https://i.imgur.com/0vp4nBV.gif)


