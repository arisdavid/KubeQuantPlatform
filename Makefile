build:
	docker build -t batch-queue-manager:latest .

vault:
    helm install vault ./vault-helm -n rqmp --set='server.dev.enabled=true'
    helm uninstall vault -n rqmp
    kubectl port-forward vault-0 8200:8200


install:
	$access_key=$(aws configure get default.aws_access_key_id)
	$secret_key=$(aws configure get default.aws_secret_access_key)
	helm install --namespace=rqmp batch-queue-manager ./charts --values ./charts/env/awsdev/values.yaml --set aws.accessKeyId=$access_key,aws.aws.secretAccessKey=$secret_key

uninstall:
	helm uninstall --namespace=rqmp batch-queue-manager
