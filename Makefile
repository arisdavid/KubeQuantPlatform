build:
	docker build -t kubequantqm:latest -f kubequantplatform/Dockerfile .

install:
	access_key=$(shell aws configure get developer.aws_access_key_id)
	secret_key=$(shell aws configure get developer.aws_secret_access_key)
	helm install --namespace=kubeq kubequantqm ./charts --values ./charts/env/awsdev/values.yaml --set AWS_ACCESS_KEY_ID=$$access_key,AWS_SECRET_ACCESS_KEY=$$secret_key

uninstall:
	helm uninstall --namespace=kubeq kubequantqm

