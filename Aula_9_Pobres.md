
# 🚦 Kubernetes Probes — Guia Prático (Startup, Liveness e Readiness)

Guia prático focado em **Kubernetes Probes** no padrão de estudo **SRE Jr**.

Este material cobre apenas:

- StartupProbe
- LivenessProbe
- ReadinessProbe

⚠️ Não confundir com **PV / PVC**, que já foram estudados anteriormente.

---

# 🎯 Objetivo da Aula

Ao final deste laboratório você será capaz de:

- Entender o papel de cada probe
- Configurar probes em um Deployment
- Identificar falhas de aplicação automaticamente
- Proteger o tráfego do usuário
- Diagnosticar problemas usando `kubectl`

---

# 🧠 Modelo Mental (Muito Importante)

Fluxo de funcionamento das Probes:

```
Container inicia
      │
      ▼
StartupProbe
(verifica se a aplicação terminou de iniciar)
      │
      ▼
LivenessProbe
(verifica se a aplicação continua saudável)
      │
      ▼
ReadinessProbe
(verifica se a aplicação pode receber tráfego)
```

Resumo rápido:

| Probe | Função |
|-----|-----|
StartupProbe | garante que a aplicação terminou de iniciar |
LivenessProbe | detecta aplicação travada |
ReadinessProbe | controla se o pod pode receber tráfego |

---

# 📦 Cenário do Laboratório

Aplicação utilizada:

```
my-app
```

Imagem:

```
bsllacerda/quarkus-examples:quarkus-mysql-connection
```

Endpoints utilizados pelas probes:

| Endpoint | Função |
|------|------|
`/startup` | verifica inicialização |
`/healthz` | verifica saúde |
`/ready` | verifica conexão com banco |

---

# 1️⃣ StartupProbe

A **StartupProbe** verifica se a aplicação **terminou de iniciar**.

Ela evita que:

- LivenessProbe mate o container muito cedo
- aplicação em inicialização seja reiniciada

Endpoint utilizado:

```
/startup
```

---

## Deployment com StartupProbe

```bash
kubectl -n config-e-persist apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: bsllacerda/quarkus-examples:quarkus-mysql-connection
        imagePullPolicy: Always
        startupProbe:
          httpGet:
            path: /startup
            port: 8080
          failureThreshold: 5
          periodSeconds: 10
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: db-credentials
        env:
        - name: INITIALIZE_PERIOD
          value: "30"
EOF
```

---

# 2️⃣ LivenessProbe

A **LivenessProbe** verifica se a aplicação **continua saudável**.

Se falhar várias vezes:

➡ Kubernetes **reinicia o container**.

Endpoint utilizado:

```
/healthz
```

---

## Deployment com LivenessProbe

```bash
kubectl -n config-e-persist apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: bsllacerda/quarkus-examples:quarkus-mysql-connection
        imagePullPolicy: Always
        startupProbe:
          httpGet:
            path: /startup
            port: 8080
          failureThreshold: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
          failureThreshold: 3
        env:
        - name: HEALTH_STATUS_OK
          value: "true"
EOF
```

---

# 3️⃣ ReadinessProbe

A **ReadinessProbe** verifica se o container **pode receber tráfego**.

Se falhar:

❌ container **não recebe tráfego**
✔ container **não é reiniciado**

Endpoint utilizado:

```
/ready
```

Este endpoint testa **conexão com MySQL**.

---

## Deployment com ReadinessProbe

```bash
kubectl -n config-e-persist apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: bsllacerda/quarkus-examples:quarkus-mysql-connection
        imagePullPolicy: Always
        startupProbe:
          httpGet:
            path: /startup
            port: 8080
          failureThreshold: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
          failureThreshold: 3
EOF
```

---

# 🔎 Observando as Probes

Monitorar Pods:

```bash
kubectl -n config-e-persist get pods -w
```

Ver logs:

```bash
kubectl -n config-e-persist logs POD_NAME -f
```

Descrever deployment:

```bash
kubectl -n config-e-persist describe deployment my-app
```

---

# 🧪 Simulando Falhas

## Falha de Liveness

Editar deployment:

```bash
kubectl -n config-e-persist edit deployment my-app
```

Alterar variável:

```
HEALTH_STATUS_OK=false
```

Resultado esperado:

➡ container reiniciado

---

## Falha de Readiness

Desligar banco:

```bash
kubectl -n config-e-persist scale deployment mysql --replicas 0
```

Resultado esperado:

```
pod Running
container Ready 0/1
```
Usuários recebem:

```
503 Service Unavailable
```

---

# 🧪 Exercícios de Fixação

### Exercício 1

Monitore as probes:

```bash
kubectl get pods -n config-e-persist -w
```

---

### Exercício 2

Veja eventos do pod:

```bash
kubectl describe pod POD_NAME
```

Identifique:

- falhas de liveness
- falhas de readiness

---

### Exercício 3

Desligue o banco:

```bash
kubectl scale deployment mysql --replicas 0 -n config-e-persist
```

Observe:

```
Ready 0/1
```

Depois religue:

```bash
kubectl scale deployment mysql --replicas 1 -n config-e-persist
```

---

# 🧹 Limpando Ambiente

```bash
kubectl delete deployment my-app -n config-e-persist
```

---

# 🧠 Resumo Final

| Probe | Reinicia container | Bloqueia tráfego |
|-----|-----|-----|
Startup | sim | sim |
Liveness | sim | não |
Readiness | não | sim |

---

# 🚀 Conclusão

As probes são essenciais para **ambientes de produção** porque permitem:

- auto recuperação
- detecção de falhas
- proteção de usuários
- maior estabilidade do cluster

Dominar probes é **habilidade obrigatória para SRE / DevOps**.
