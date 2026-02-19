# 🚀 Kubernetes - Estudos Práticos | Bruno Mori

Repositório com exercícios práticos, documentação e comandos de Kubernetes, organizados de forma progressiva.

Foco em:
- Uso real de `kubectl`
- Manifestos YAML
- Deployments e Rollouts
- Escalabilidade
- Namespaces
- Networking
- Mentalidade operacional (SRE)

---

# 📘 Estrutura do Repositório

| Aula | Tema |
|------|------|
| Aula 1 | Containers e Conceitos Básicos |
| Aula 2 | Pods |
| Aula 3 | ReplicaSets |
| Aula 4 | Deployments |
| Aula 4.1 | Rollback |
| Aula 4.2 | Rollout |
| Aula 4.3 | Autoscaler (HPA) |
| Aula 5 | Namespaces |
| Aula 6 | Networking |
| Comandos | Referência prática de kubectl |

---

# 🎯 Objetivo

Consolidar fundamentos de Kubernetes com prática real de terminal, criação de recursos e troubleshooting básico.

Este repositório não é apenas teoria — todos os comandos foram executados em cluster local.

---

# 🛠 Tecnologias Utilizadas

- Kubernetes
- kubectl
- YAML
- Minikube / Kind (ambiente local)
- Containers (Docker runtime)

---

# 🧱 Conceitos Estudados

## 📦 Containers
- O que é container
- Diferença entre imagem e container
- Execução isolada

## 🟢 Pods
- Estrutura básica
- Containers dentro do pod
- Logs e describe
- Debug básico

## 🔁 ReplicaSet
- Garantia de número mínimo de réplicas
- Labels e selectors
- Alta disponibilidade básica

## 🚀 Deployments
- Atualizações controladas
- Estratégia Rolling Update
- Histórico de revisões

## 🔄 Rollout & Rollback
- Verificar status
- Desfazer versões
- Estratégia segura de atualização

## 📈 Autoscaler (HPA)
- Escalabilidade horizontal
- CPU-based scaling
- Ajuste de mínimo e máximo de réplicas

## 🏷 Namespaces
- Separação de ambientes
- Contexto atual
- Isolamento lógico

## 🌐 Networking
- ClusterIP
- NodePort
- Comunicação entre pods
- Conceito de Service

---

# 🔧 Comandos Mais Utilizados

```bash
# Pods
kubectl get pods
kubectl describe pod <nome>
kubectl logs <nome>

# Deployments
kubectl get deployments
kubectl rollout status deployment/<nome>
kubectl rollout undo deployment/<nome>

# Autoscaler
kubectl autoscale deployment <nome> --min=1 --max=5 --cpu-percent=50

# Namespaces
kubectl create namespace dev
kubectl config set-context --current --namespace=dev
