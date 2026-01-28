# 📘 Aula 4.3 – Deployments

## Aplicando alterações de forma controlada (rollout pause e rollout resume)

---

## 🎯 Objetivo da aula

* Entender o uso de **rollout pause** e **rollout resume**
* Aplicar **múltiplas alterações de forma controlada**
* Evitar rollouts parciais durante manutenções
* Consolidar alterações em **um único rollout**

---

## 🔧 Pré-requisitos

* Deployment `my-nginx-app` existente
* Kubernetes em execução
* `kubectl` configurado corretamente

---

## 1️⃣ Preparação e monitoramento

Limpe os terminais e inicie o monitoramento dos recursos.

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

* Deployment estável
* Pods em estado `Running`

---

## 2️⃣ Pausando o rollout do Deployment

Vamos pausar o rollout para aplicar alterações sem que o Kubernetes crie novos Pods imediatamente.

```bash
kubectl rollout pause deployment/my-nginx-app
```

📌 **O que acontece**

* O Deployment entra em estado **paused**
* Alterações podem ser feitas sem disparar rollout

---

## 3️⃣ Primeira manutenção – Atualizar versão do NGinx

Atualizar a imagem para a versão `stable-alpine`.

```bash
kubectl set image deployment/my-nginx-app nginx=nginx:stable-alpine
```

📌 Nenhum novo Pod é criado neste momento.

---

## 4️⃣ Segunda manutenção – Ajustar recursos do container

Vamos definir limites de CPU e memória.

```bash
kubectl set resources deployment/my-nginx-app \
  -c=nginx \
  --limits=cpu=150m,memory=256Mi
```

📌 Mesmo após duas alterações, **nenhum rollout ocorre** porque o Deployment está pausado.

---

## 5️⃣ Retomando o rollout (aplicando tudo de uma vez)

Agora vamos liberar o Deployment para aplicar todas as alterações simultaneamente.

```bash
kubectl rollout resume deployment/my-nginx-app
```

📌 **O Kubernetes irá**

* Criar um novo ReplicaSet
* Substituir os Pods antigos
* Aplicar imagem + recursos em um único rollout

---

## 6️⃣ Verificando IPs dos Pods

```bash
kubectl get pods -o=yaml | grep podIP
```

---

## 7️⃣ Verificar versão do NGinx

Acesse um dos Pods usando o IP obtido.

```bash
curl -i [podIP]
```

📌 **Resultado esperado**

* Header indicando **NGinx versão 1.24 (stable-alpine)**

---

## 8️⃣ Registrar a alteração no histórico (change-cause)

```bash
kubectl annotate deployment/my-nginx-app \
  kubernetes.io/change-cause="Deploy OK - Nginx version stable-alpine + resource limits"
```

---

## 9️⃣ Verificar histórico de rollout

```bash
kubectl rollout history deployment my-nginx-app
```

📌 O histórico agora registra a alteração consolidada.

---

## 🧠 Conceitos aprendidos

* `rollout pause` bloqueia rollouts automáticos
* Múltiplas alterações podem ser feitas com segurança
* `rollout resume` aplica tudo em um único rollout
* Técnica ideal para **janelas de manutenção**
* Evita estados intermediários inconsistentes

---

## 🔗 Referência oficial

* Kubernetes Deployments – Rollout
* [https://kubernetes.io/docs/concepts/workloads/controllers/deployment/](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
