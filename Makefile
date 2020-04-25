build:
	docker build -t task-queue-manager:latest .

install:
	# access_key=$(shell aws configure get developer.aws_access_key_id)
	# secret_key=$(shell aws configure get developer.aws_secret_access_key) 
	# helm install --namespace=rqmp tqm-chart ./tqm-chart --values ./tqm-chart/env/dev/values.yaml --set aws.accessKeyId=$$access_key,aws.aws.secretAccessKey=$$secret_key
	helm install --namespace=rqmp tqm-chart ./tqm-chart --values ./tqm-chart/env/dev/values.yaml
uninstall:
	helm uninstall --namespace=rqmp tqm-chart

