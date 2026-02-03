# 📘 Aula 4.3 – Deployments
## Scale Manual e Horizontal Pod Autoscaler (HPA)

---

## 🎯 Objetivo da Aula

- Entender **scale manual** (scale in / scale out)
- Entender o **Horizontal Pod Autoscaler (HPA)**
- Saber quem tem precedência: **scale manual x HPA**
- Praticar **criação, verificação e remoção** de recursos
- Usar **manifestos YAML apenas como complemento**, não como foco principal

> 💡 Importante: nesta aula, **aplicar HPA direto via comando é mais importante**
> do que editar manifesto. A parte de YAML fica **no final**, como apoio profissional.

---

## 🔧 Pré-requisitos

- Deployment `my-nginx-app`
- Cluster Kubernetes ativo
- `kubectl` configurado

---

## 1️⃣ Monitoramento do Deployment

    kubectl get pods
    kubectl get pods -w
    kubectl get rs
    kubectl get rs -w
    kubectl rollout status deployment/my-nginx-app

📌 Esperado: Deployment com **3 réplicas** em estado `Running`.

---

## 2️⃣ Scale Manual

### 🔼 Scale Out (3 → 5)

    kubectl scale deployment/my-nginx-app --replicas=5
    kubectl get pods

### 🔽 Scale In (5 → 1)

    kubectl scale deployment/my-nginx-app --replicas=1
    kubectl get pods
    kubectl get deployment my-nginx-app

📌 Scale manual altera apenas o campo `replicas` do Deployment.

---

## 3️⃣ Criar Horizontal Pod Autoscaler (HPA)

    kubectl autoscale deployment/my-nginx-app \
      --min=3 \
      --max=5 \
      --cpu-percent=90

📌 O HPA:
- Garante **mínimo de 3 Pods**
- Escala até **5 Pods**
- Usa **CPU** como métrica

---

## 4️⃣ Precedência: HPA x Scale Manual

    kubectl scale deployment/my-nginx-app --replicas=4
    kubectl scale deployment/my-nginx-app --replicas=1

📌 Resultado: o HPA ignora o scale manual e mantém **3 réplicas**.

💡 **Regra:** HPA ativo **sempre sobrescreve** o scale manual.

---

## 5️⃣ Verificar HPA

    kubectl get hpa my-nginx-app

---

## 6️⃣ Exemplo adicional de criação de HPA

    kubectl autoscale deployment myy \
      --min=3 \
      --max=5 \
      --cpu=90%

---

## 7️⃣ Remover Recursos

    kubectl delete deployment my-nginx-app
    kubectl delete hpa my-nginx-app

    kubectl get deployment
    kubectl get rs
    kubectl get hpa

---

## ⚡ Comandos Essenciais — Deployment

    kubectl create deployment meu-deploy --image=nginx
    kubectl delete deployment meu-deploy
    kubectl get deployment

---

## 🧠 Conceitos-Chave

- Scale manual ajusta `replicas` diretamente
- HPA controla réplicas automaticamente
- HPA tem **prioridade total** sobre scale manual
- Comandos diretos são os mais usados no dia a dia
- YAML serve para **backup, versionamento e recriação**

---

## 📝 Exercício de Fixação

1. Crie um Deployment `nginx-scale` com imagem `nginx`
2. Escale manualmente para **5** e depois para **2** réplicas
3. Crie um HPA:
   - min: 1
   - max: 5
   - CPU: 50%
4. Tente fazer scale manual com o HPA ativo
5. Explique: **quem manda e por quê**

---

## 📄 Via Manifesto (Complementar)

> Apoio profissional. **Não é o foco principal da aula.**

---

## 8️⃣ Gerar e Salvar Manifestos

    kubectl autoscale deployment/my-nginx-app \
      --min=3 \
      --max=5 \
      --cpu-percent=90 \
      --dry-run=client -o yaml \
      > /root/aplicacoes/deployments/my-nginx-hpa.yaml

    kubectl get deployment my-nginx-app -o yaml \
      > /root/aplicacoes/deployments/my-nginx-deployment-v2.yaml

---

## 9️⃣ Recriar Recursos via YAML

    kubectl apply -f /root/aplicacoes/deployments/my-nginx-deployment-v2.yaml
    kubectl apply -f /root/aplicacoes/deployments/my-nginx-hpa.yaml

---

## 🔟 Editar Manifestos

### Deployment (`my-nginx-deployment-v2.yaml`)
- `revisionHistoryLimit: 2`
- Imagem: `nginx:stable-alpine`

### HPA (`my-nginx-hpa.yaml`)
- `maxReplicas: 12`

---

## 🧹 Limpeza Final

    kubectl delete -f /root/aplicacoes/deployments/my-nginx-deployment-v2.yaml
    kubectl delete -f /root/aplicacoes/deployments/my-nginx-hpa.yaml
    kubectl get all

---

## 🔗 Referência

- Kubernetes Docs — Horizontal Pod Autoscaler
