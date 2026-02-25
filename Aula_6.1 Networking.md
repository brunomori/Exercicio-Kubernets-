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

# 🧪 Exercício SRE Mode — Ciclo Completo de Services

## 🎯 Objetivo

Treinar:

- Diferença prática entre **ClusterIP**, **NodePort** e **LoadBalancer**
- Comportamento interno vs externo
- Relação **Service ↔ Pods ↔ ReplicaSet**
- Troubleshooting básico

---

# 🔁 PARTE 1 — Reset do Ambiente

```bash
kubectl delete svc --all
kubectl delete deployment pacman
```

Confirme que está limpo:

```bash
kubectl get all
```

---

# 🔵 PARTE 2 — ClusterIP (Rede Interna)

## 1️⃣ Crie o Deployment

```bash
kubectl create deployment pacman \
--image=bsllacerda/pacman \
--replicas=3
```

## 2️⃣ Crie o Service ClusterIP

```bash
kubectl expose deployment pacman \
--port=80 \
--target-port=80 \
--name=pacman-clusterip \
--type=ClusterIP
```

## 3️⃣ Valide

```bash
kubectl get svc
kubectl get endpoints
kubectl describe svc pacman-clusterip
```

---

## 🧠 Perguntas críticas

- O Service tem IP?
- Ele tem `EXTERNAL-IP`?
- Ele cria porta externa?
- Se eu deletar 1 Pod, o que acontece com os endpoints?

---

# 🟡 PARTE 3 — NodePort (Exposição Controlada)

## 1️⃣ Delete apenas o Service

```bash
kubectl delete svc pacman-clusterip
```

> O Deployment continua rodando.

## 2️⃣ Crie o NodePort

```bash
kubectl expose deployment pacman \
--port=80 \
--target-port=80 \
--name=pacman-nodeport \
--type=NodePort
```

## 3️⃣ Valide

```bash
kubectl get svc
kubectl describe svc pacman-nodeport
```

---

## 🧠 Perguntas críticas

- Qual porta foi aberta?
- Essa porta existe dentro do Pod?
- Se você trocar de nó (em cluster real), funciona?
- Qual a diferença estrutural real entre ClusterIP e NodePort?

---

# 🔴 PARTE 4 — LoadBalancer (Cloud Simulation)

## 1️⃣ Delete NodePort

```bash
kubectl delete svc pacman-nodeport
```

## 2️⃣ Crie LoadBalancer

```bash
kubectl expose deployment pacman \
--port=80 \
--target-port=80 \
--name=pacman-loadbalancer \
--type=LoadBalancer
```

## 3️⃣ Observe

```bash
kubectl get svc
```

---

## 🧠 Perguntas críticas

- Aparece `EXTERNAL-IP`?
- Por que fica `<pending>`?
- Em cloud, o que aconteceria aqui?
- Internamente ele ainda é um ClusterIP?

---

# 🔥 PARTE 5 — Teste de Resiliência (Mentalidade SRE)

Agora o teste mais importante:

```bash
kubectl delete pod <um-pod-qualquer>
```

Depois:

```bash
kubectl get pods
kubectl get endpoints
```

---

## 🧠 Perguntas fundamentais

- O Service caiu?
- Por que não caiu?
- Quem garante que novos Pods apareçam?
- O Service depende do Pod ou de labels?

> Se você responder isso corretamente, você entendeu 70% do conceito real de Service.

---

# 🧠 Resumo Conceitual (Fixação)

| Tipo          | Interno | Externo | Depende de Cloud | Uso Real              |
|--------------|----------|----------|------------------|-----------------------|
| ClusterIP     | ✅       | ❌       | ❌               | Comunicação interna   |
| NodePort      | ✅       | ✅       | ❌               | Labs / testes         |
| LoadBalancer  | ✅       | ✅       | ✅               | Produção              |

---

# 🎯 Missão Final (Modo SRE Real)

Sem olhar nada, explique com suas palavras:

- O que é um Service?
- Ele cria container?
- Ele roda código?
- Ele sabe que Pods existem como?
- O que acontece se o label do Pod não bater com o selector?

---

Se você responder isso com segurança,  
você não está mais estudando Kubernetes.

Você está entendendo Kubernetes.
