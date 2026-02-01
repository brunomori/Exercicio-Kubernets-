# Aula 4 – Kubernetes: Deployments, Rollout e Restart

Nesta aula entramos no **recurso MAIS usado em produção no Kubernetes**: **Deployment**.

Tudo aqui é a **evolução natural** das aulas anteriores:

**Pod → ReplicaSet → Deployment**

Adaptado para:

- Ubuntu
- Usuário comum
- kubectl (Docker como runtime já configurado)

---

## 🎯 Objetivo da aula

- Criar um Deployment
- Entender a relação Deployment → ReplicaSet → Pods
- Monitorar rollout
- Ver status da implantação
- Usar rollout restart
- Trabalhar com histórico de versões

---

## 🧠 Conceito-chave (decora isso)

> Deployment é o controlador de mais alto nível para aplicações stateless.

Ele:

- cria ReplicaSets
- controla Pods
- permite rollout, rollback e restart

Em produção você usa Deployment, não Pod nem ReplicaSet direto.

---

## 1️⃣ Pré-configuração (simulando a aula)

Abra **3 terminais**:

### Terminal 1 – Monitorar ReplicaSets

    kubectl get rs -w

### Terminal 2 – Monitorar Pods

    kubectl get pods -w

### Terminal 3 – Execução dos comandos

---

## 2️⃣ Criar estrutura de pastas

    mkdir -p ~/k8s/deployments
    cd ~/k8s/deployments

---

## 3️⃣ Criar o manifesto do Deployment (imperativo)

Gerar o YAML usando o kubectl (boa prática):

    kubectl create deployment my-nginx-app \
      --image=nginx:1.14.2 \
      --replicas=3 \
      --dry-run=client -o yaml > my-nginx-deployment.yaml

Esse comando:

- cria um Deployment
- define a imagem
- define a quantidade de réplicas
- apenas gera o YAML (não aplica no cluster)

---

## 4️⃣ Verificar o manifesto criado

    cat my-nginx-deployment.yaml

Observe:

- kind: Deployment
- replicas: 3
- template → definição dos Pods

---

## 5️⃣ Aplicar o Deployment

    kubectl apply -f my-nginx-deployment.yaml

Fluxo criado automaticamente:

Deployment → ReplicaSet → Pods

---

## 6️⃣ Verificar o status do Rollout

    kubectl rollout status deployment/my-nginx-app

---

## 7️⃣ Inspecionar o Deployment

    kubectl get deployment my-nginx-app
    kubectl get deployment my-nginx-app -o wide

---

## 8️⃣ Descrever o Deployment

    kubectl describe deployment my-nginx-app

Aqui você vê:

- eventos
- estado das réplicas
- ReplicaSet controlado

---

## 9️⃣ Histórico de Rollout

    kubectl rollout history deployment my-nginx-app

---

## 🔟 Rollout Restart

Reiniciar os Pods sem alterar a imagem:

    kubectl rollout restart deployment my-nginx-app

O que acontece:

- novos Pods sobem
- Pods antigos são finalizados
- sem downtime

---

## 🧹 Limpeza do ambiente (refazer a aula do zero)

Ao final da aula, remova o Deployment para poder repetir todo o processo novamente.

### Deletar o Deployment

    kubectl delete deployment my-nginx-app


## 🧠 Conceitos fixados nesta aula

- Deployment é o padrão em produção
- ReplicaSet é gerenciado automaticamente
- Pods são descartáveis
- Rollout acompanha implantações
- Restart recria Pods com segurança
- Hierarquia: Deployment → RS → Pods

---

## ⚠️ Observação de mercado

- Não gerencie Pods diretamente
- Não use kubectl run em produção
- Sempre use Deployment

---

## 🔁 Exercício de fixação

1. Criar um Deployment com 3 réplicas
2. Monitorar Pods e ReplicaSets
3. Verificar rollout status
4. Executar rollout restart
5. Conferir o histórico
