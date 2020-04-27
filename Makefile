build:
	docker build -t batch-queue-manager:latest .
install:
    helm install --namespace=rqmp batch-queue-manager ./charts --values ./charts/env/awsdev/values.yaml
uninstall:
    helm uninstall --namespace=rqmp batch-queue-manager
