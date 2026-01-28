# 📘 Aula 4.1 – Deployments

## Rollback, Rollout History e Rollout Undo

---

## 🎯 Objetivo da aula

* Simular uma **falha durante um deploy**
* Entender o comportamento do **Deployment**, **ReplicaSets** e **Pods**
* Consultar o **histórico de versões (rollout history)**
* Executar **rollback** para uma versão estável da aplicação

---

## 🔧 Pré-requisitos

* Deployment `my-nginx-app` criado na Aula 4
* Kubernetes em execução
* `kubectl` configurado e funcional

---

## 1️⃣ Preparação do ambiente e monitoramento

Limpe os terminais e organize o monitoramento.

### Monitorar Pods

```bash
kubectl get pods
kubectl get pods -w
```

### Monitorar ReplicaSets

```bash
kubectl get rs
kubectl get rs -w
```

### Monitorar status do Deployment

```bash
kubectl rollout status deployment/my-nginx-app
```

📌 **Resultado esperado**

* Pods em estado `Running`
* Um ReplicaSet ativo com 3 réplicas prontas

---

## 2️⃣ Simulando falha no Deployment

Vamos atualizar a imagem do Deployment para uma versão **inexistente**.

```bash
kubectl set image deployment/my-nginx-app nginx=nginx:inexistente
```

📌 **O que acontece**

* Um novo rollout é iniciado imediatamente
* Um novo ReplicaSet é criado
* Os novos Pods entram em estado de erro (`ImagePullBackOff` ou `ErrImagePull`)
* O Kubernetes **mantém os Pods antigos funcionando**

---

## 3️⃣ Análise do problema

### Verificar o estado do Deployment

```bash
kubectl get deployment my-nginx-app
```

### Descrever o Deployment

```bash
kubectl describe deployment my-nginx-app
```

📌 **Observe**

* Réplicas desejadas: 3
* Réplicas disponíveis: 3 (versão antiga)
* Réplicas com erro: Pods do novo ReplicaSet

💡 Isso demonstra o funcionamento correto do **RollingUpdate**.

---

## 4️⃣ Registrar a falha no histórico (Change Cause)

Registrar a causa da mudança é uma boa prática em ambientes profissionais.

```bash
kubectl annotate deployment/my-nginx-app \
  kubernetes.io/change-cause="Deploy Failure - Nginx version inexistente"
```

---

## 5️⃣ Consultar histórico de versões (Rollout History)

```bash
kubectl rollout history deployment/my-nginx-app
```

📌 **Exemplo de saída**

```
REVISION  CHANGE-CAUSE
1         Deploy OK - Nginx version 1.14.2
2         Deploy Failure - Nginx version inexistente
```

---

## 6️⃣ Executar Rollback para versão estável

Agora vamos retornar para a versão funcional da aplicação.

```bash
kubectl rollout undo deployment/my-nginx-app --to-revision=1
```

📌 **O Kubernetes irá**

* Cancelar o rollout com falha
* Reativar o ReplicaSet da versão estável
* Remover os Pods problemáticos

---

## 7️⃣ Verificação pós-rollback

### Verificar status do Deployment

```bash
kubectl rollout status deployment/my-nginx-app
```

### Verificar Pods

```bash
kubectl get pods
```

### Verificar ReplicaSets

```bash
kubectl get rs
```

✅ **Resultado esperado**

* Todos os Pods em estado `Running`
* Apenas um ReplicaSet ativo
* Deployment estável

---

## 🧠 Conceitos aprendidos

* Deployments criam e gerenciam ReplicaSets automaticamente
* Rollouts são iniciados automaticamente ao alterar a imagem
* O Kubernetes mantém versões estáveis em caso de falha
* Rollback é rápido e seguro
* O uso de `change-cause` facilita auditoria e troubleshooting

---

## 🔗 Referência oficial

* Kubernetes Deployments
* [https://kubernetes.io/docs/concepts/workloads/controllers/deployment/](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
