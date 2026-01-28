# Aula 4 – Kubernetes: Deployments, Rollout e Restart

Nesta aula entramos no **recurso MAIS usado em produção no Kubernetes**: **Deployment**.

Tudo aqui é a **evolução natural** das aulas anteriores (Pod → ReplicaSet → Deployment).

Adaptado para:

* Ubuntu
* usuário comum
* kubectl (Docker como runtime já configurado)

---

## 🎯 Objetivo da aula

* Criar um **Deployment**
* Entender a relação **Deployment → ReplicaSet → Pods**
* Monitorar **rollout**
* Ver status da implantação
* Usar **rollout restart**
* Trabalhar com histórico de versões

---

## 🧠 Conceito-chave (decora isso)

> **Deployment é o controlador de mais alto nível para aplicações stateless.**

Ele:

* cria ReplicaSets
* controla Pods
* permite rollout, rollback e restart

👉 **Em produção você usa Deployment, não Pod nem ReplicaSet direto.**

---

## 1️⃣ Pré-configuração (simulando a aula)

Abra **4 terminais**:

### Terminal 1 – Monitorar ReplicaSets

```bash
kubectl get rs -w
```

### Terminal 2 – Monitorar Pods

```bash
kubectl get pods -w
```

### Terminal 3 – Execução dos comandos

### Terminal 4 – Apoio (curl / inspeções)

---

## 2️⃣ Criar estrutura de pastas

📌 Aula original:

```
/root/aplicacoes/deployments/
```

📌 Adaptado:

```bash
mkdir -p ~/k8s/deployments
cd ~/k8s/deployments
```

---

## 3️⃣ Criar o manifesto do Deployment (imperativo)

Vamos gerar o YAML usando o kubectl (boa prática):

```bash
kubectl create deployment my-nginx-app \
  --image=nginx:1.14.2 \
  --replicas=3 \
  --dry-run=client -o yaml > my-nginx-deployment.yaml
```

📌 O que esse comando faz:

* **create deployment** → cria um Deployment
* **--image** → imagem do container
* **--replicas** → quantidade inicial
* **--dry-run** → não aplica, só gera o YAML
* **-o yaml** → saída em YAML

---

## 4️⃣ Verificar o manifesto criado

```bash
cat my-nginx-deployment.yaml
```

📌 Observe:

* `kind: Deployment`
* `replicas: 3`
* `template` (mesmo conceito do ReplicaSet)

---

## 5️⃣ Aplicar o Deployment

```bash
kubectl apply -f my-nginx-deployment.yaml
```

Observe nos terminais:

* Deployment cria um ReplicaSet
* ReplicaSet cria os Pods

---

## 6️⃣ Verificar o status do Rollout

```bash
kubectl rollout status deployment/my-nginx-app
```

✅ Indica se a aplicação foi implantada com sucesso.

---

## 7️⃣ Inspecionar o Deployment

```bash
kubectl get deployment my-nginx-app
kubectl get deployment my-nginx-app -o wide
kubectl get deployment my-nginx-app -o wide --show-labels
```

---

## 8️⃣ Descrever o Deployment

```bash
kubectl describe deployment my-nginx-app
```

📌 Aqui você vê:

* eventos
* replicas
* estratégia de rollout

---

## 9️⃣ Verificar IPs dos Pods

```bash
kubectl get pods -o yaml | grep podIP
```

📌 Cada Pod tem **seu próprio IP** dentro do cluster.

---

## 🔟 Verificar versão do Nginx

Escolha um podIP e execute:

```bash
curl -i <POD_IP>
```

Verifique o header:

```
Server: nginx/1.14.2
```

---

## 1️⃣1️⃣ Histórico de Rollout

```bash
kubectl rollout history deployment my-nginx-app
```

---

## 1️⃣2️⃣ Anotar causa da mudança

```bash
kubectl annotate deployment/my-nginx-app \
  kubernetes.io/change-cause="Deploy OK - Nginx version 1.14.2"
```

Verificar novamente:

```bash
kubectl rollout history deployment my-nginx-app
```

---

## 1️⃣3️⃣ Rollout Restart

Reiniciar a aplicação sem mudar a imagem:

```bash
kubectl rollout restart deployment my-nginx-app
```

Observe:

* novos Pods sendo criados
* Pods antigos sendo finalizados

---

## 🧠 Conceitos fixados nesta aula

* Deployment é o **controle principal** da aplicação
* Rollout acompanha a implantação
* Restart sem downtime
* Histórico de versões
* Relação Deployment → RS → Pods

---

## ⚠️ Observação de mercado

* Nunca use `kubectl run` em produção
* Nunca gerencie Pod direto
* **Deployment é padrão**

---

## 🔁 Exercício de fixação

1. Crie o Deployment
2. Observe RS e Pods
3. Veja rollout status
4. Faça rollout restart
5. Consulte o histórico

Se fizer sem olhar, você está **no nível profissional** ✅

---

## 🔜 Próxima aula

* Atualização de versão (rollout update)
* Rollback
* Estratégias de deployment
