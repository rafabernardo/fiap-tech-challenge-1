# Tech Challenge do curso Pós-Tech - Software Architecture | FIAP

## Guia Passo a Passo para Criar o Cluster e Executar os Comandos

Este guia irá orientá-lo no processo de criação de um cluster Kubernetes e na execução dos comandos necessários para implantar sua aplicação.

### Pré-requisitos

- [Docker](https://docs.docker.com/engine/install/) instalado
- [KIND](https://kind.sigs.k8s.io/docs/user/quick-start/) (Kubernetes in Docker) instalado
- [Kubectl](https://kubernetes.io/docs/tasks/tools/) instalado

### Passos

1. **Criar Cluster Kubernetes com Kind**

   ```sh
   make kind-create-cluster
   ```

   **Descrição**: Este comando cria um cluster Kubernetes local usando Kind.

2. **Construir Imagem Docker Local**

   ```sh
   make docker-build-local-image
   ```

   **Descrição**: Este comando constrói a imagem Docker para a aplicação localmente.

3. **Carregar Imagem Docker no Cluster Kind**

   ```sh
   make kind-load-image
   ```

   **Descrição**: Este comando carrega a imagem Docker construída localmente no cluster Kind.

4. **Aplicar Implantação Local**

   ```sh
   make k-apply-local-deployment
   ```

   **Descrição**: Este comando aplica a configuração de implantação local no cluster Kubernetes.

5. **Aplicar Configuração de Serviço**

   ```sh
   make k-apply-svc
   ```

   **Descrição**: Este comando aplica a configuração de serviço para expor a aplicação dentro do cluster Kubernetes.

6. **Aplicar Configuração de Ingress**

   ```sh
   make k-apply-ingress
   ```

   **Descrição**: Este comando aplica a configuração de ingress para gerenciar o acesso externo aos serviços no cluster Kubernetes.

7. **Aplicar Autoscaler Horizontal de Pods (HPA)**

   ```sh
   make k-apply-hpa
   ```

   **Descrição**: Este comando aplica a configuração do HPA para escalar automaticamente o número de pods com base na utilização da CPU.

8. **Criar Config Map**

   ```sh
   make k-create-config-map
   ```

   **Descrição**: Este comando cria um ConfigMap no Kubernetes para armazenar dados de configuração.

9. **Deletar Config Map**

   ```sh
   make k-delete-config-map
   ```

   **Descrição**: Este comando deleta o ConfigMap do Kubernetes.

10. **Criar Docker Secret**

    ```sh
    make k-create-docker-secret
    ```

    **Descrição**: Este comando cria um segredo Docker no Kubernetes para puxar imagens de um registro Docker privado.

11. **Deletar Docker Secret**

    ```sh
    make k-delete-docker-secret
    ```

    **Descrição**: Este comando deleta o segredo Docker do Kubernetes.

12. **Aplicar Controlador de Ingress NGINX**

    ```sh
    make k-apply-nginx-ingress
    ```

    **Descrição**: Este comando aplica a configuração do Controlador de Ingress NGINX para gerenciar o acesso externo aos serviços.

13. **Aplicar Servidor de Métricas**

    ```sh
    make k-apply-metric-svc
    ```

    **Descrição**: Este comando aplica a configuração do Servidor de Métricas para habilitar métricas de uso de recursos no cluster Kubernetes.

14. **Patch no Servidor de Métricas**

    ```sh
    make k-apply-patch-metric-svc
    ```

    **Descrição**: Este comando aplica um patch na configuração do Servidor de Métricas para garantir que ele funcione corretamente com o cluster Kubernetes.

15. **Aplicar migration com Alembic**

    ```sh
      make k-apply-migration
    ```

    **Descrição**: Este comando aplica a migration no banco de dados.

### Conclusão

Seguindo esses passos, você terá um cluster Kubernetes totalmente funcional com sua aplicação implantada e configurada. Cada comando desempenha um papel crucial na configuração do ambiente, implantação da aplicação e garantia de que ela funcione sem problemas.

---
