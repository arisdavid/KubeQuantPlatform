dev-configure:
	pip3 install -r dev-requirements.txt
	pre-commit install
	pre-commit install --hook-type commit-msg
build:
	docker build -t kubequantqm:latest -f kubequantplatform/Dockerfile .
install-vault:
	helm install vault . --set='server.dev.enabled=true'
uninstall-vault:
	helm uninstall vault ./vault-helm
install:
	helm install kubequantqm ./charts --values ./charts/env/awsdev/values.yaml
uninstall:
	helm uninstall kubequantqm




