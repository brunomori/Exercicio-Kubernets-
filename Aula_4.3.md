# 📘 Aula 4.3 – Deployments

## Scale e Horizontal Pod Autoscaler (HPA)

---

## 🎯 Objetivo

* Entender **scale manual (scale in / scale out)**
* Entender o **Horizontal Pod Autoscaler (HPA)**
* Saber quem manda: **scale manual x HPA**
* Praticar **backup, edição e recriação** de recursos via YAML

---

## 🔧 Pré-requisitos

* Deployment `my-nginx-app`
* Cluster Kubernetes ativo
* `kubectl` configurado

---

## 1️⃣ Monitoramento

```bash
kubectl get pods
kubectl get pods -w
kubectl get rs
kubectl get rs -w
kubectl rollout status deployment/my-nginx-app
```

📌 Esperado: Deployment com **3 réplicas** em `Running`.

---

## 2️⃣ Scale manual

### Scale Out (3 → 5)

```bash
kubectl scale deployment/my-nginx-app --replicas=5
kubectl get pods
```

### Scale In (5 → 1)

```bash
kubectl scale deployment/my-nginx-app --replicas=1
kubectl get pods
kubectl get deployment my-nginx-app
```

📌 Scale manual altera apenas o campo `replicas` do Deployment.

---

## 3️⃣ Criar HPA

```bash
kubectl autoscale deployment/my-nginx-app \
  --min=3 \
  --max=5 \
  --cpu-percent=90
```

📌 O HPA garante **mínimo 3 Pods** e escala até **5** conforme CPU.

---

## 4️⃣ Precedência do HPA

```bash
kubectl scale deployment/my-nginx-app --replicas=4
kubectl scale deployment/my-nginx-app --replicas=1
```

📌 Resultado: o HPA ignora o scale manual e mantém **3 réplicas**.

💡 **Regra:** HPA ativo **sempre sobrescreve** o scale manual.

---

## 5️⃣ Verificar HPA

```bash
kubectl get hpa my-nginx-app
```

---

## 6️⃣ Gerar e salvar manifestos

```bash
kubectl autoscale deployment/my-nginx-app \
  --min=3 \
  --max=5 \
  --cpu-percent=90 \
  --dry-run=client -o yaml \
  > /root/aplicacoes/deployments/my-nginx-hpa.yaml

kubectl get deployment my-nginx-app -o yaml \
  > /root/aplicacoes/deployments/my-nginx-deployment-v2.yaml
```

📌 Prática profissional de **backup e versionamento**.

---

## 7️⃣ Remover recursos

```bash
kubectl delete deployment my-nginx-app
kubectl delete hpa my-nginx-app
```

---

## 8️⃣ Editar manifestos

**Deployment** (`my-nginx-deployment-v2.yaml`):

* `revisionHistoryLimit: 2`
* imagem: `nginx:stable-alpine`

**HPA** (`my-nginx-hpa.yaml`):

* `maxReplicas: 12`

---

## 9️⃣ Recriar recursos

```bash
kubectl apply -f /root/aplicacoes/deployments/my-nginx-deployment-v2.yaml
kubectl apply -f /root/aplicacoes/deployments/my-nginx-hpa.yaml
```

```bash
kubectl get deployment
kubectl get rs
kubectl get hpa
```

---

## 🔟 Limpeza final

```bash
kubectl delete -f /root/aplicacoes/deployments/my-nginx-deployment-v2.yaml
kubectl delete -f /root/aplicacoes/deployments/my-nginx-hpa.yaml
kubectl get all
```

---

## ⚡ Comandos Essenciais — Criar, Deletar e Conferir Deployment

```bash
kubectl create deployment meu-deploy --image=nginx

```
```bash
kubectl delete deployment meu-deploy
```
```bash
kubectl get deployment
```


## 🧠 Conceitos-chave

* Scale manual = ajuste direto de `replicas`
* HPA controla replicas automaticamente
* HPA tem prioridade sobre scale manual
* YAML permite backup, recriação e rollback

---

## 📝 Exercício rápido

1. Crie um Deployment `nginx-scale` com imagem `nginx`
2. Escale manualmente para 5 e depois para 2 réplicas
3. Crie um HPA:

   * min: 1 | max: 5 | CPU: 50%
4. Tente fazer scale manual com HPA ativo
5. Explique: **quem manda e por quê**

---

## 🔗 Referência

* Kubernetes Docs — Horizontal Pod Autoscaler
