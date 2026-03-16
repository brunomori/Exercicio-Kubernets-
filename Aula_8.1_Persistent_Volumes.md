
# 💾 Kubernetes Volumes, PersistentVolumes (PV) e PersistentVolumeClaims (PVC)

Guia prático para entender **armazenamento persistente no Kubernetes** utilizando
PV e PVC com um exemplo real implantando **MySQL**.

---

# 🎯 Objetivo da Aula

Ao final desta prática você será capaz de:

- Entender como funciona **armazenamento persistente no Kubernetes**
- Criar um **PersistentVolume (PV)**
- Criar um **PersistentVolumeClaim (PVC)**
- Montar o volume dentro de um **Deployment**
- Garantir que **dados sobrevivam ao reinício dos Pods**

---

# 📦 Cenário do Laboratório

Iremos:

1. Criar um diretório no node
2. Criar um **PersistentVolume**
3. Criar um **PersistentVolumeClaim**
4. Implantar um **MySQL usando o PVC**
5. Expor o banco usando um **Service**
6. Validar que os dados estão persistindo

---

# 📁 Etapa 1 — Criar diretório que será usado como Volume

O volume será armazenado no node local.

```bash
sudo mkdir -p /mnt/disks/vol1
```

Verifique:

```bash
ls -la /mnt/disks
```

---

# 🧱 Etapa 2 — Criar o PersistentVolume

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mysql-pv
spec:
  capacity:
    storage: 1Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-path
  local:
    path: /mnt/disks/vol1
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - rocky.local
EOF
```

Verifique o PV:

```bash
kubectl get pv
```

---

# 📄 Etapa 3 — Criar PersistentVolumeClaim

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
  namespace: config-e-persist
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: local-path
  resources:
    requests:
      storage: 1Gi
EOF
```

Verifique:

```bash
kubectl -n config-e-persist get pvc
```

Verifique também o diretório do volume:

```bash
ls -la /mnt/disks/vol1
```

Neste momento o diretório ainda estará vazio.

---

# 🐬 Etapa 4 — Criar Deployment do MySQL

```bash
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
  namespace: config-e-persist
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:5.7
        volumeMounts:
        - name: mysql-storage
          mountPath: /var/lib/mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: PASSWORD
        - name: MYSQL_USER
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: USERNAME
        - name: MYSQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: PASSWORD
        - name: MYSQL_DATABASE
          value: testdb
      volumes:
      - name: mysql-storage
        persistentVolumeClaim:
          claimName: mysql-pvc
EOF
```

Verifique o Pod:

```bash
kubectl get pods -n config-e-persist
```

Agora verifique novamente o diretório:

```bash
ls -la /mnt/disks/vol1
```

Agora arquivos do **MySQL aparecerão no diretório**.

---

# 🌐 Etapa 5 — Expor o MySQL com Service

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: mysql
  namespace: config-e-persist
spec:
  selector:
    app: mysql
  ports:
  - protocol: TCP
    port: 3306
    targetPort: 3306
EOF
```

Verifique:

```bash
kubectl -n config-e-persist get svc
```

---

# 🔎 Validação

Confira novamente:

```bash
kubectl get pv
kubectl -n config-e-persist get pvc
ls -la /mnt/disks/vol1
```

Mesmo que o **Pod seja recriado**, os dados permanecerão.

Isso ocorre porque:

```
Pod → PVC → PV → Disco do Node
```

---

# 🧪 Exercícios de Fixação

### 1️⃣ Ver logs do MySQL

```bash
kubectl logs -n config-e-persist deployment/mysql
```

---

### 2️⃣ Deletar o Deployment

```bash
kubectl -n config-e-persist delete deployment mysql
```

Agora verifique:

```bash
ls -la /mnt/disks/vol1
```

Os dados **continuam no disco**.

---

### 3️⃣ Recriar o Deployment

Reaplique o manifesto do MySQL e veja que os dados voltam a ser utilizados.

---

# 🧹 Limpando o Ambiente

```bash
kubectl -n config-e-persist delete svc mysql
kubectl -n config-e-persist delete deployment mysql
kubectl -n config-e-persist delete pvc mysql-pvc
kubectl delete pv mysql-pv
sudo rm -rf /mnt/disks
```

---

# 🧠 Resumo Mental (Muito Importante)

```
Container (efêmero)
      ↓
Volume Mount
      ↓
PVC (Pedido de armazenamento)
      ↓
PV (Volume real)
      ↓
Disco do Node / Storage
```

---

# 🚀 Conclusão

Agora você aprendeu um dos **conceitos mais importantes do Kubernetes para produção**:

✔ Persistência de dados  
✔ Separação entre compute e storage  
✔ Uso de PV e PVC  

Esses conceitos são fundamentais para operar:

- Bancos de dados
- Filas
- Sistemas de cache
- Aplicações stateful

