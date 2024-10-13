Guide: [GPT chat](https://chatgpt.com/share/66f9bacc-a798-800b-ad31-fc2bb0a6fe4b)

Install [Kubectl](https://kubernetes.io/docs/tasks/tools/)
Install [KIND](https://kind.sigs.k8s.io/docs/user/quick-start/)

Create cluster

```bash
$ kind create cluster -n cluster-name
$ # kind create cluster --config infrastructure/kubernetes/cluster.yaml
```

Set dockerhub-secret to download the app Docker image

```bash
$ kubectl create secret docker-registry dockerhub-secret \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=<your-username> \
  --docker-password=<your-password>
```

Set env-config to use .env on deploy

```bash
$ kubectl create configmap env-config --from-env-file=.env
```

Install and Ingress controller

```bash
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Create pods, services and ingress

```bash
$ kubectl apply -f infrastructure/kubernetes/deployment-local.yaml
$ # kubectl apply -f infrastructure/kubernetes/deployment-prod.yaml
$ kubectl apply -f infrastructure/kubernetes/service.yaml
$ kubectl apply -f infrastructure/kubernetes/ingress.yaml
$ kubectl apply -f infrastructure/kubernetes/hpa.yaml
```