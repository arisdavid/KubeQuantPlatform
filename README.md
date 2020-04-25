## Risk Quant Model Platform
![CircleCI](https://circleci.com/gh/arisdavid/RiskQuantModelPlatform/tree/master.svg?style=shield&circle-token=4497d0b6994553429ad830631fbde0e5762aab67)

## Introduction
Risk Quant Model Platform (RQMP) is an experimental model execution platform. 
The platform is responsible for for creating and orchestrating ephemeral pods with containerised quantitative models inside the cluster. 
 
 
## Local Development

#### Requirements
* Docker
* Kubernetes (K8s)
* Minikube
* Kubectl 
* Python3.7
* AWS Cloud [WIP]

#### Initial Setup

Create a virtual environment and activate it:
```
python -m venv venv
```

Install the app requirements:
```
pip3 install -r requirements.txt
```

Install the dev-requirements:
```
pip3 install -r dev-requirements.txt
```

#### Kubernetes Local Development
Minikube is a tool that makes it easy for developer to use and run Kubernetes cluster locally.  
It’s a great way to quickly get a cluster up & running so you can start interacting with the K8s API.

Setup a Kubernetes cluster using minikube. 

https://kubernetes.io/docs/setup/learning-environment/minikube/

Launch a minikube cluster using the following command:
```
minikube start 
```

Create a namespace:
```
kubectl create namespace <namespace_name>
```

Set the namespace context to the namespace created from the previous step:
```
kubectl config set-context $(kubectl config current-context) --namespace=<namespace_name>
```

Ensure you're inside the Kubernetes environment as this is where the images will be built:
 
```
eval $(minikube docker-env)
```


#### Docker Images

Clone the the the repositories and build the corresponding Docker images inside the Kubernetes cluster:

* Geometric Brownian Motion (GBM) - a model to forecast price paths given expected sigma and expected return. https://github.com/arisdavid/rqmp-credit-risk-models
  
    ```
    docker build -t market-risk-models:latest .
    ```
    
* KMV - a model to calculate the probability of a company defaulting. https://github.com/arisdavid/rqmp-market-risk-models

    ```
    docker build -t credit-models:latest .
    ```


#### Local execution

Execute the command below from the RiskQuantModelPlatform project root:

##### KMV Model
```
python main.py kmv 1000000 900000 500000 0.18 0.12
```

##### Monte Carlo Simulation of Geometric Brownian Motion Model

```
python main.py mcs gbm 1000 200 0.2 0.18 365 250
```


## AWS Development [WIP]

#### AWS Resources
Spin up AWS Resources through Terraform.

##### Terraform Plan
##### Terraform Apply

#### Helm 
Helm is a tool for managing Kubernetes charts. Charts are packages of pre-configured Kubernetes resources.
To install Helm, refer to the Helm install guide and ensure that the helm binary is in the PATH of your shell:

https://helm.sh/docs/intro/install/


#### Docker Images
Follow the same steps above for building the models' docker images. 

Build the Batch-Queue-Manager image from the root project of this repository:

```
docker build -t batch-queue-manager:latest .
```


## Optional Tools
* `k9s` for interacting with the cluster. I find k9s UI dashboard to be handy  - https://github.com/derailed/k9s. 
* Terminal. Sometimes I'd switch between my Windows Desktop and Mac. I find these terminals to help with productivity.
  * Windows
    * ConEmu with powershell bash
  * Mac
    * Iterm2 with ZSH and oh-my-zsh
    
    ![![Image of K9s]](https://i.imgur.com/0vp4nBV.gif)

