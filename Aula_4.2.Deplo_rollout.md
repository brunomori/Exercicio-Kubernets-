# 📘 Aula 4.2 – Deployments

## Aplicando alterações de forma controlada (rollout pause e rollout resume, aumentar recusos computacional )

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

# Exercício de Fixação — Rollout Pause e Rollout Resume

## Objetivo
Fixar o uso dos comandos **rollout pause** e **rollout resume** para aplicar múltiplas alterações de forma controlada em um Deployment.

---

## Parte 1 — Preparação

1. Utilize um Deployment existente chamado `my-nginx-app`.
2. Verifique o status atual do Deployment.
3. Liste os Pods e os ReplicaSets relacionados ao Deployment.

---

## Parte 2 — Pausando o Rollout

4. Pause o rollout do Deployment `my-nginx-app`.
5. Confirme que o Deployment está pausado.
6. Atualize a imagem do container `nginx` para a versão `nginx:stable-alpine`.
7. Atualize também os limites de recursos do container:
   - CPU: 150m  
   - Memória: 256Mi
8. Observe que **nenhum novo Pod** é criado enquanto o rollout estiver pausado.

---

## Parte 3 — Retomando o Rollout

9. Retome o rollout do Deployment.
10. Acompanhe a criação dos novos Pods.
11. Verifique o status final do Deployment.
12. Obtenha o IP de um Pod e valide a versão do Nginx via `curl`.

---

## Parte 4 — Fixação Conceitual

Responda mentalmente ou anote:

13. Por que utilizar `rollout pause` antes de aplicar múltiplas alterações?
14. O que acontece se você esquecer de executar o `rollout resume`?
15. Qual a vantagem desse processo em ambientes de produção?

---

## Observações
- `rollout pause` permite agrupar alterações.
- `rollout resume` aplica todas as mudanças de uma única vez.
- Essa prática reduz riscos durante manutenções.

---

