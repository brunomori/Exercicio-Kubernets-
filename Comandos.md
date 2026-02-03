# 🚀 Guia Rápido de Comandos Kubernetes (SRE Júnior)

> Guia **prático, direto e de consulta rápida**, no estilo **README para GitHub**, focado no dia a dia de um **SRE Júnior**.

---

## 📌 Pré-requisitos

* `kubectl` instalado
* Acesso a um cluster Kubernetes

Verificar conexão com o cluster:

```bash
kubectl cluster-info
kubectl get nodes
```

---

## 🧱 Conceitos Essenciais (bem direto)

* **Cluster** → Conjunto de máquinas que rodam o Kubernetes
* **Node** → Máquina (VM ou física)
* **Pod** → Menor unidade (1 ou mais containers)
* **Deployment** → Gerencia Pods (escala, restart, updates)
* **Service** → Expõe Pods na rede
* **Namespace** → Isolamento lógico

---

## 📦 Comandos Básicos de Observação (90% do uso)

### Ver recursos

```bash
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get nodes
```

Com mais detalhes:

```bash
kubectl get pods -o wide
```

Por namespace:

```bash
kubectl get pods -n kube-system
```

---

## 🔍 Inspeção e Diagnóstico

### Descrever recursos (DEBUG)

```bash
kubectl describe pod <nome-do-pod>
kubectl describe deployment <nome>
```

### Logs

```bash
kubectl logs <pod>
```

Container específico:

```bash
kubectl logs <pod> -c <container>
```

Logs em tempo real:

```bash
kubectl logs -f <pod>
```

---

## 🛠️ Execução dentro do Pod

Entrar no container:

```bash
kubectl exec -it <pod> -- /bin/sh
```

Se tiver bash:

```bash
kubectl exec -it <pod> -- /bin/bash
```

---

## 📄 Aplicar e Gerenciar Manifests

### Criar / Atualizar recursos

```bash
kubectl apply -f arquivo.yaml
```

Aplicar uma pasta inteira:

```bash
kubectl apply -f ./k8s/
```

### Remover recursos

```bash
kubectl delete -f arquivo.yaml
```

---

## 🔁 Deployments (Escala e Controle)

### Ver deployments

```bash
kubectl get deployments
```

### Escala manual

```bash
kubectl scale deployment <nome> --replicas=3
```

### Ver rollout

```bash
kubectl rollout status deployment <nome>
```

### Rollback

```bash
kubectl rollout undo deployment <nome>
```

---

## 🌐 Services

Ver services:

```bash
kubectl get svc
```

Tipos comuns:

* `ClusterIP` (interno)
* `NodePort` (exposição simples)
* `LoadBalancer` (cloud)

---

## 📂 Namespaces

Listar:

```bash
kubectl get ns
```

Usar namespace específico:

```bash
kubectl get pods -n <namespace>
```

Definir namespace padrão:

```bash
kubectl config set-context --current --namespace=<namespace>
```

---

## ⚠️ Comandos de Emergência (SRE raiz 😅)

### Deletar pod travado (ele recria sozinho se tiver Deployment)

```bash
kubectl delete pod <pod>
```

### Forçar delete

```bash
kubectl delete pod <pod> --grace-period=0 --force
```

---

## 🧪 Checklist Rápido de Incidente

1. `kubectl get pods`
2. `kubectl describe pod <pod>`
3. `kubectl logs <pod>`
4. Ver eventos:

```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

---

## 🎯 Exercício de Fixação (rápido)

1. Liste todos os Pods
2. Escolha um Pod e veja os logs
3. Entre no Pod com `exec`
4. Escale um Deployment para 2 réplicas
5. Delete um Pod e veja ele recriar

---

## 📎 Dica Final de SRE Júnior

> **Se você sabe observar, descrever e ler logs, você já resolve 70% dos incidentes.**

Esse guia é para **consulta diária**. Conforme evoluir para SRE pleno, você vai automatizar tudo isso.

---

✅ Pronto para versionar no GitHub como `README.md`.
