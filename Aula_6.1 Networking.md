# 📘 Aula -- Kubernetes Services (ClusterIP, NodePort e LoadBalancer)

## 🎯 Objetivo

Entender na prática os 3 principais tipos de Service no Kubernetes:

-   ClusterIP
-   NodePort
-   LoadBalancer

Vamos usar a aplicação Pacman (`bsllacerda/pacman`) como exemplo.

------------------------------------------------------------------------

# 🧱 Pré-requisito

Você já deve ter um Deployment rodando:

``` bash
kubectl create deployment pacman \
--image=bsllacerda/pacman \
--replicas=3
```

Verifique:

``` bash
kubectl get pods
kubectl get deployments
```

------------------------------------------------------------------------

# 🔵 1️⃣ ClusterIP Service

## 📌 Conceito

-   Tipo padrão do Kubernetes
-   Expõe a aplicação apenas dentro do cluster
-   Recebe um IP interno (ClusterIP)
-   Não é acessível externamente pelo navegador

## Criando o Service

``` bash
kubectl expose deployment pacman \
--port=80 \
--target-port=80 \
--name=pacman-clusterip-svc \
--type=ClusterIP
```

## Monitorando

``` bash
kubectl get svc -o wide
```

## Testando internamente

``` bash
kubectl describe svc pacman-clusterip-svc
curl <CLUSTER-IP>
```

## Gerando YAML

``` bash
kubectl expose deployment pacman \
--port=80 \
--target-port=80 \
--name=pacman-clusterip-svc \
--type=ClusterIP \
--dry-run=client -o yaml > pacman-clusterip-svc.yaml
```

------------------------------------------------------------------------

# 🟡 2️⃣ NodePort Service

## 📌 Conceito

-   Abre uma porta entre 30000--32767
-   Acessível via IP-DA-VM:NodePort
-   Funciona em ambientes locais

## Criando o Service

``` bash
kubectl expose deployment pacman \
--port=80 \
--target-port=80 \
--name=pacman-nodeport-svc \
--type=NodePort
```

## Verificando porta atribuída

``` bash
kubectl describe svc pacman-nodeport-svc
kubectl get svc
```

## Acessando

http://IP-DA-VM:NodePort

## Gerando YAML

``` bash
kubectl expose deployment pacman \
--port=80 \
--target-port=80 \
--name=pacman-nodeport-svc \
--type=NodePort \
--dry-run=client -o yaml > pacman-nodeport-svc.yaml
```

------------------------------------------------------------------------

# 🔴 3️⃣ LoadBalancer Service

## 📌 Conceito

-   Utilizado em provedores Cloud
-   Cria automaticamente um Load Balancer externo
-   Em ambiente local normalmente ficará como `<pending>`{=html}

## Criando o Service

``` bash
kubectl expose deployment pacman \
--port=80 \
--target-port=80 \
--name=pacman-loadbalancer-svc \
--type=LoadBalancer
```

## Verificando

``` bash
kubectl get svc
```

## Gerando YAML

``` bash
kubectl expose deployment pacman \
--port=80 \
--target-port=80 \
--name=pacman-loadbalancer-svc \
--type=LoadBalancer \
--dry-run=client -o yaml > pacman-loadbalancer-svc.yaml
```

------------------------------------------------------------------------

# 🧠 Comparação Final

  Tipo           Acesso Externo   Uso Comum
  -------------- ---------------- -----------------------
  ClusterIP      ❌ Não           Comunicação interna
  NodePort       ✅ Sim           Labs / Ambiente local
  LoadBalancer   ✅ Sim           Produção em Cloud

------------------------------------------------------------------------

# 🧪 Exercício de Fixação

1.  Delete o NodePort:

    ``` bash
    kubectl delete svc pacman-nodeport-svc
    ```

2.  Delete um Pod:

    ``` bash
    kubectl delete pod <nome-do-pod>
    ```

3.  Perguntas:

    -   O Service para de funcionar?
    -   Por que não?
