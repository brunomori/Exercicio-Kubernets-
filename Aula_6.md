# 📘 Aula 6 – Networking no Kubernetes (Services + DNS)

## 🎯 Objetivo da Aula
- Entender **como Pods se comunicam**
- Aprender **por que Service é essencial**
- Conhecer os principais tipos de `Service`
- Entender **DNS no Kubernetes**
- Criar um **modelo mental de troubleshooting de rede**

---

## 🔧 Conceito Essencial (sem rodeio)

- Pods **têm IP**, mas são **efêmeros**
- IP de Pod **muda**
- **Nunca** acesse Pods diretamente em produção
- `Service` é quem garante **acesso estável**
- DNS conecta **nome → Service → Pods**

👉 Networking no Kubernetes = **Service + DNS**

---

## 🧠 Modelo Mental (guarde isso)

Usuário / App  
→ Service (nome fixo)  
→ Pods (IP muda, Service resolve)

---

## 1️⃣ Comunicação entre Pods

Todo Pod recebe um IP próprio:

    kubectl get pods -o wide

📌 Pods conseguem se comunicar **diretamente por IP**, mesmo em nodes diferentes.  
⚠️ Mas **não é prática recomendada** usar IP de Pod.

---

## 2️⃣ O que é um Service?

`Service` é um recurso que:
- Cria um **endpoint estável**
- Faz **load balance** entre Pods
- Resolve o problema do IP dinâmico

👉 Service **não roda container**, ele só aponta para Pods via **labels**.

---

## 3️⃣ Tipos de Service (o que importa agora)

### 🔹 ClusterIP (padrão)
- Acesso **interno ao cluster**
- Mais usado
- Base de tudo

### 🔹 NodePort
- Expõe porta do node
- Pouco usado em produção
- Mais comum em estudo/lab

### 🔹 LoadBalancer
- Cria IP externo (cloud)
- Depende do provedor (AWS, GCP, etc)

📌 Para SRE Jr: **ClusterIP é obrigatório dominar**.

---

## 4️⃣ Criando um Service ClusterIP (exemplo)

Supondo Pods com label `app=nginx`:

    kubectl expose pod nginx --port=80 --name=nginx-svc

Verificar o Service criado:

    kubectl get svc
    kubectl describe svc nginx-svc

📌 Observe:
- `Type: ClusterIP`
- `Endpoints` apontando para os Pods

---

## 5️⃣ Service funciona por Labels

Se o Service não encontra Pods, **não é bug de rede**, é label errada.

Ver labels do Pod:

    kubectl get pod nginx --show-labels

Ver selector do Service:

    kubectl describe svc nginx-svc

👉 Selector precisa **bater exatamente** com a label.

---

## 6️⃣ DNS no Kubernetes (CoreDNS)

Todo Service gera automaticamente um nome DNS.

Formato padrão:

    <service>.<namespace>.svc.cluster.local

Exemplo:

    nginx-svc.default.svc.cluster.local

Dentro do cluster, **use o nome**, nunca IP.

---

## 7️⃣ Testando DNS na prática

Criar um Pod temporário para teste:

    kubectl run dns-test --image=busybox -- sleep 3600

Entrar no Pod:

    kubectl exec -it dns-test -- sh

Testar resolução DNS:

    nslookup nginx-svc

📌 Se resolve o nome, o DNS está funcionando.

---

## 8️⃣ Ordem correta de troubleshooting de rede

Sempre siga essa ordem:

1. Namespace certo?
2. Pod está `Running`?
3. Pod tem IP?
4. Service existe?
5. Service tem `Endpoints`?
6. Labels batem?
7. DNS resolve?

👉 80% dos problemas acabam aqui.

---

## 9️⃣ Erros comuns (e reais)

- Olhar Pod no namespace errado
- Service sem endpoints
- Label errada no Deployment
- Acessar IP do Pod direto
- Esquecer que Service é interno por padrão

---

## 🧪 Exercício de Fixação (Essencial)

1. Crie um Pod nginx
2. Verifique o IP do Pod
3. Crie um Service ClusterIP para ele
4. Liste os Services
5. Verifique os Endpoints do Service
6. Crie um Pod busybox para teste
7. Resolva o nome DNS do Service
8. Delete os recursos criados

Comandos de referência:

    kubectl run nginx --image=nginx
    kubectl get pods -o wide
    kubectl expose pod nginx --port=80 --name=nginx-svc
    kubectl get svc
    kubectl describe svc nginx-svc
    kubectl run dns-test --image=busybox -- sleep 3600
    kubectl exec -it dns-test -- sh
    nslookup nginx-svc

🔥 Se você entende por que **Service existe** e **nunca usa IP de Pod**, você entendeu networking básico no Kubernetes.
