# Aula 3 – Kubernetes: ReplicaSet na prática

Nesta aula vamos sair do **Pod isolado** e entrar no conceito de **alta disponibilidade** usando **ReplicaSet**.

Tudo aqui é **adaptado para Ubuntu + usuário comum**, mantendo **100% do conceito da aula original**.

---

## 🎯 Objetivo da aula

* Entender o que é um **ReplicaSet**
* Criar múltiplos Pods automaticamente
* Observar o comportamento de **auto-recuperação**
* Escalar réplicas manualmente
* Encerrar a aplicação corretamente

---

## 🧠 Conceito rápido (decora isso)

> **ReplicaSet garante que X Pods estejam sempre rodando.**
> Se um Pod morrer, o Kubernetes cria outro.

📌 Você **não gerencia Pods diretamente** — o ReplicaSet faz isso por você.

---

## 1️⃣ Pré-configuração (simulando a aula)

📌 A aula pede vários terminais. No Ubuntu, a ideia é a mesma.

### Terminal 1 – Monitorar Pods (deixe aberto)

```bash
kubectl get pods -w
```

### Terminal 2 – Executar os comandos

Use este para os próximos passos.

---

## 2️⃣ Criar a estrutura de pastas

📌 Aula original:

```
/root/aplicacoes/replicasets/
```

📌 Adaptado:

```bash
mkdir -p ~/k8s/replicasets
cd ~/k8s/replicasets
```

Conferir:

```bash
pwd
ls -l
```

---

## 3️⃣ Criar o manifesto do ReplicaSet

```bash
cat > my-app-rs.yaml << EOF
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: my-app
  labels:
    app: my-app
    tier: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: my-app
        image: nginx
EOF
```

---

## 4️⃣ Conferir o manifesto

```bash
cat my-app-rs.yaml
```

📌 Esse arquivo define **estado desejado**: 3 Pods Nginx.

---

## 5️⃣ Aplicar o ReplicaSet

```bash
kubectl apply -f my-app-rs.yaml
```

Observe no terminal de monitoramento:

* Pods sendo criados automaticamente

---

## 6️⃣ Listar ReplicaSets

```bash
kubectl get rs
```

---

## 7️⃣ Teste de auto-recuperação (ESSENCIAL)

Apague **um Pod** manualmente:

```bash
kubectl delete pod <nome-de-um-pod>
```

🔍 O que acontece:

* O ReplicaSet detecta
* Um **novo Pod é criado automaticamente**

👉 Esse é o coração do Kubernetes.

---

## 8️⃣ Escalar a aplicação (3 → 5 réplicas)

Editar o ReplicaSet:

```bash
kubectl edit rs my-app
```

Altere:

```yaml
replicas: 5
```

Salvar e sair.

Observe os novos Pods surgindo.

---

## 9️⃣ Desligar a aplicação (réplicas = 0)

Editar novamente:

```bash
kubectl edit rs my-app
```

Alterar para:

```yaml
replicas: 0
```

Resultado:

* Todos os Pods são encerrados

---

## 🔟 Limpeza do ambiente

Excluir o ReplicaSet:

```bash
kubectl delete rs my-app
```

Conferir:

```bash
kubectl get rs
kubectl get pods
```

---

Se sua intenção for PARAR os pods

## 🔻 Escalar para zero

```bash
kubectl scale rs my-app --replicas=0
```

Você vai ver todos indo para Terminating e nenhum voltando.

## 🔥 Ou deletar o ReplicaSet

```bash
kubectl delete rs my-app
```

## 🧠 Conceitos fixados nesta aula

* ReplicaSet mantém **quantidade desejada de Pods**
* Auto-healing (auto-recuperação)
* Escalabilidade manual
* Pods são **descartáveis**
* YAML define o estado desejado

---

## ⚠️ Observação importante (nível mercado)

👉 **Não se usa ReplicaSet direto em produção.**

Quem cria ReplicaSet automaticamente é o:

* **Deployment** ✅ (próxima aula)

ReplicaSet é importante para:

* entender o funcionamento interno
* prova / certificação
* base conceitual

---

## 🔁 Exercício de fixação

1. Crie o ReplicaSet
2. Apague Pods
3. Escale para 5
4. Reduza para 0
5. Delete o RS

Se fizer sem olhar, você **entendeu Kubernetes de verdade** 🚀

---

## 🔜 Próxima aula

* Deployment
* Rollout
* Rollback
* Versionamento de aplicação
