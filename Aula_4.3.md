# 📘 Aula 4.2 – Deployments

## Scale e Horizontal Pod Autoscaler (HPA)

---

## 🎯 Objetivo da aula

* Entender **scale manual (scale in / scale out)**
* Explorar o **Horizontal Pod Autoscaler (HPA)**
* Compreender precedência entre **scale manual x HPA**
* Gerar e reutilizar **manifestos a partir de objetos existentes**
* Simular um fluxo real de **backup, edição e recriação de recursos**

---

## 🔧 Pré-requisitos

* Deployment `my-nginx-app` criado nas aulas anteriores
* Kubernetes em execução
* `kubectl` configurado

---

## 1️⃣ Preparação e monitoramento

Organize os terminais e inicie o monitoramento.

### Pods

```bash
kubectl get pods
kubectl get pods -w
```

### ReplicaSets

```bash
kubectl get rs
kubectl get rs -w
```

### Status do Deployment

```bash
kubectl rollout status deployment/my-nginx-app
```

📌 **Estado esperado**

* Deployment com 3 réplicas
* Pods em estado `Running`

---

## 2️⃣ Scale manual – Scale Out (3 → 5)

```bash
kubectl scale deployment/my-nginx-app --replicas=5
```

### Verificar Pods

```bash
kubectl get pods
```

📌 **Resultado esperado**

* 5 Pods em execução

---

## 3️⃣ Scale manual – Scale In (5 → 1)

```bash
kubectl scale deployment/my-nginx-app --replicas=1
```

### Verificar Pods e Deployment

```bash
kubectl get pods
kubectl get deployment my-nginx-app
```

📌 **Resultado esperado**

* Apenas 1 Pod ativo

---

## 4️⃣ Criando o Horizontal Pod Autoscaler (HPA)

O HPA controla automaticamente o número de réplicas com base no uso de CPU.

```bash
kubectl autoscale deployment/my-nginx-app \
  --min=3 \
  --max=5 \
  --cpu-percent=90
```

📌 **Comportamento esperado**

* O Deployment passa a manter **mínimo de 3 Pods**
* Pode escalar automaticamente até **5 Pods**

---

## 5️⃣ Testando precedência do HPA

### Tentar escalar manualmente para 4

```bash
kubectl scale deployment/my-nginx-app --replicas=4
```

➡️ O HPA ajusta novamente para o mínimo configurado.

### Tentar escalar para 1

```bash
kubectl scale deployment/my-nginx-app --replicas=1
```

📌 **Resultado**

* Nada acontece
* O HPA mantém **3 réplicas**

💡 **Conclusão:**

> Quando existe HPA, ele tem **precedência total** sobre o campo `replicas` do Deployment.

---

## 6️⃣ Verificando o HPA

```bash
kubectl get hpa my-nginx-app
```

---

## 7️⃣ Gerar manifesto do HPA (dry-run)

```bash
kubectl autoscale deployment/my-nginx-app \
  --min=3 \
  --max=5 \
  --cpu-percent=90 \
  --dry-run=client -o yaml \
  > /root/aplicacoes/deployments/my-nginx-hpa.yaml
```

### Ver manifesto

```bash
vim /root/aplicacoes/deployments/my-nginx-hpa.yaml
```

---

## 8️⃣ Backup dos manifestos atuais (Deployment e HPA)

```bash
kubectl get deployment my-nginx-app -o yaml \
  > /root/aplicacoes/deployments/my-nginx-deployment-v2.yaml

kubectl get hpa my-nginx-app -o yaml \
  > /root/aplicacoes/deployments/my-nginx-hpa-v2.yaml
```

💡 Técnica essencial para **backup e rollback manual**.

---

## 9️⃣ Remover recursos via comandos imperativos

```bash
kubectl delete deployment my-nginx-app
kubectl delete hpa my-nginx-app
```

---

## 🔟 Editar manifestos (versão 2)

### Deployment

```bash
vim /root/aplicacoes/deployments/my-nginx-deployment-v2.yaml
```

* Ajustar:

  * `revisionHistoryLimit: 2`
  * imagem para `nginx:stable-alpine`

### HPA

```bash
vim /root/aplicacoes/deployments/my-nginx-hpa-v2.yaml
```

* Ajustar:

  * `maxReplicas: 12`

---

## 1️⃣1️⃣ Recriar recursos a partir dos manifestos

```bash
kubectl apply -f /root/aplicacoes/deployments/my-nginx-deployment-v2.yaml
kubectl apply -f /root/aplicacoes/deployments/my-nginx-hpa-v2.yaml
```

### Verificar estado

```bash
kubectl get deployment
kubectl get rs
kubectl get hpa
```

---

## 1️⃣2️⃣ Limpeza do ambiente usando manifestos

```bash
kubectl delete -f /root/aplicacoes/deployments/my-nginx-deployment-v2.yaml
kubectl delete -f /root/aplicacoes/deployments/my-nginx-hpa-v2.yaml
```

### Conferir limpeza

```bash
kubectl get all
```

---

## 🧠 Conceitos fixados

* Scale manual altera o campo `replicas`
* HPA sobrescreve o controle manual
* HPA trabalha baseado em métricas (CPU)
* Backup de manifestos é prática profissional
* Recursos podem ser recriados fielmente via YAML

---

## 🔗 Referências

* HPA – Kubernetes
* [https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
