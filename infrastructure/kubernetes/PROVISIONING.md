Guide: [GPT chat](https://chatgpt.com/share/66f9bacc-a798-800b-ad31-fc2bb0a6fe4b)


Install [Kubectl](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)
Install [KIND](https://kind.sigs.k8s.io/docs/user/quick-start/)

Create cluster
```bash
$ kind create cluster -n cluster-name
```

Install and Ingress controller
```bash
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

Create pods, services and ingress
```bash
$ kubectl apply infrastructure/deployment.yaml
$ kubectl apply infrastructure/service.yaml
$ kubectl apply infrastructure/ingress.yaml
$ kubectl apply infrastructure/hpa.yaml
```

```bash
$ kubectl port-forward svc/service-name <mapped-port>:<node-port>
$ # kubectl port-forward svc/service-name 8080:80
$ # it may be needed becouse of missconfiguration between Ingress and NGINX
```

Set env-config to use .env on deploy
```bash
$ kubectl create configmap env-config --from-env-file=.env
```