## Kube Quant Platform
[![CircleCI](https://circleci.com/gh/arisdavid/KubeQuantPlatform/tree/master.svg?style=shield&circle-token=4497d0b6994553429ad830631fbde0e5762aab67)](https://circleci.com/gh/arisdavid/KubeQuantPlatform/tree/master)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Introduction
Kube Quant Platform is an experimental model execution platform. 
The platform is responsible for creating and orchestrating ephemeral pods with containerised quant models inside a Kubernetes cluster. 
 

## Local Development

#### Tooling Requirements

* Docker - For building container image
* Minikube - "Playground" Kubernetes cluster
* Kubectl - CLI tool for controlling kubernetes cluster
* Vault - Identity and secret management
* AWSCLI - CLI tool for interacting with AWS
* Terraform - Spinning up cloud resources


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


#### Docker Images (Sample Quant Models)

Clone the the the repositories and build the corresponding Docker images inside the Kubernetes cluster:

* Geometric Brownian Motion (GBM) - a model to forecast price paths given expected sigma and expected return. https://github.com/arisdavid/rqmp-market-risk-models
  
    ```
    docker build -t market-risk-models:latest .
    ```
    
* KMV - a model to calculate the probability of a company defaulting. https://github.com/arisdavid/rqmp-credit-risk-models

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

## AWS Development and Testing (WIP)

#### Vault Configuration

We are using vault to store secrets and inject them into the pods as when needed e.g. Cloud credential. 

Clone Vault-Helm repository - https://github.com/hashicorp/vault-k8s

Ensure the current context is set to namespace=<namespace_name> you're currently working on. 

Install vault:
```
helm install vault ./vault-helm --set='server.dev.enabled=true   
```

`Optional` - Create a port forward 8200:8200. The UI becomes accessible at host:8200:

```
kubectl port-forward vault-0 8200:8200 
```

Access vault's shell (vault-0 is the pod's name):
```
kubectl exec -it vault-0 /bin/sh
```

Create a read policy applicable to secret:
```
cat <<EOF> /home/vault/app-policy.hcl
path "secret*" {
    capabilities = ["read"]
}
EOF
```

```
vault policy write app /home/vault/app-policy.hcl
```


Configure the vault Kubernetes Auth Method:
```
vault auth enable kubernetes
```

Bind the policy to the application service account:

```
vault write auth/kubernetes/config \
    token_reviewer_jwt="$(cat var/run/secrets/kubernetes.io/serviceaccount/token)" \
    kubernetes_host=https://${KUBERNETES_PORT_443_TCP_ADDR}:443 \
    kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
```

```
vault write auth/kubernetes/role/myapp \
    bound_service_account_names=<app_service_account> \
    bound_service_account_namespaces=<namespace> \
    policies=app \
    ttl=1h
 
```

Create the AWS secrets: 
```
vault kv put secret/aws AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> \
                        AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> \
                        AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>
```


#### AWS Resources (TODO)

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

