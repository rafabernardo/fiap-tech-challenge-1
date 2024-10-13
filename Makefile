include .env

API_PORT ?= 8000

build:
	docker compose build

run:
	docker compose up -d

stop:
	docker compose down

remove:
	docker compose rm -f

clean-up: 
	docker compose down -v

start-up: run


# Kubernetes

kind-create-cluster:
	kind create cluster --config infrastructure/kubernetes/cluster.yaml

kind-load-image:
	kind load docker-image local:image

k-apply-prod-deployment:
	kubectl apply -f infrastructure/kubernetes/deployment-prod.yaml

k-apply-local-deployment:
	kubectl apply -f infrastructure/kubernetes/deployment-local.yaml

k-apply-svc:
	kubectl apply -f infrastructure/kubernetes/service.yaml

k-apply-ingress:
	kubectl apply -f infrastructure/kubernetes/ingress.yaml

k-apply-hpa:
	kubectl apply -f infrastructure/kubernetes/hpa.yaml
	
k-create-config-map:
	kubectl create configmap env-config --from-env-file=.env

k-delete-config-map:
	kubectl delete configmap env-config

k-create-docker-secret:
	kubectl create secret docker-registry dockerhub-secret \
	--docker-server=https://index.docker.io/v1/ \
	--docker-username=$(username) \
	--docker-password==$(password)

k-delete-docker-secret:
	kubectl delete secret dockerhub-secret