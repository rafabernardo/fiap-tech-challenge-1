Install [Kubectl](https://kubernetes.io/docs/tasks/tools/)
Install [KIND](https://kind.sigs.k8s.io/docs/user/quick-start/)

Create cluster

```bash
$ kind create cluster -n cluster-name
$ # kind create cluster --config infrastructure/kubernetes/cluster.yaml
```

Set dockerhub-secret to download the app Docker image
Only needed to private repositories

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

Add metrics-server to monitoring resources

```bash
 $ kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.5.0/components.yaml
 $ kubectl patch -n kube-system deployment metrics-server --type=json \
  -p '[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
```
