# 🚀 Kubernetes —  SRE | Bruno Mori

> Referência de consulta rápida: comandos, YAMLs mínimos, troubleshooting e flags úteis.
> Baseado nos estudos práticos das Aulas 1–9.

---

## 📑 Índice

| # | Tema |
|---|------|
| 1 | [Pods](#-pods) |
| 2 | [ReplicaSets](#-replicasets) |
| 3 | [Deployments](#-deployments) |
| 4 | [Rollout & Rollback](#-rollout--rollback) |
| 5 | [HPA — Autoscaler](#-hpa--autoscaler) |
| 6 | [Namespaces](#-namespaces) |
| 7 | [Networking — Services](#-networking--services) |
| 8 | [Ingress](#-ingress) |
| 9 | [ConfigMaps & Secrets](#-configmaps--secrets) |
| 10 | [Volumes, PV e PVC](#-volumes-pv-e-pvc) |
| 11 | [Helm](#-helm) |
| 12 | [YAMLs Mínimos](#-yamls-mínimos) |
| 13 | [Troubleshooting Rápido](#-troubleshooting-rápido) |
| 14 | [Flags Úteis](#-flags-úteis) |

---

## 🟢 Pods

```bash
kubectl get pods                          # listar pods
kubectl get pods -n <namespace>           # pods de um namespace específico
kubectl get pods -A                       # pods de todos os namespaces
kubectl get pods -o wide                  # exibe node e IP
kubectl describe pod <nome>               # detalhes completos + eventos
kubectl logs <nome>                       # logs do pod
kubectl logs <nome> -c <container>        # logs de container específico
kubectl logs <nome> --previous            # logs do container que morreu
kubectl exec -it <nome> -- bash           # shell interativo no pod
kubectl exec -it <nome> -- sh             # quando não tem bash
kubectl delete pod <nome>                 # deletar pod
kubectl run nginx --image=nginx           # criar pod rápido (imperativo)
```

---

## 🔁 ReplicaSets

```bash
kubectl get replicasets                   # listar replicasets
kubectl describe replicaset <nome>        # detalhes + eventos
kubectl delete replicaset <nome>          # deletar (pods junto)
kubectl scale replicaset <nome> --replicas=5  # escalar manualmente
```

---

## 🚀 Deployments

```bash
kubectl get deployments                   # listar deployments
kubectl describe deployment <nome>        # detalhes completos
kubectl apply -f deployment.yaml          # aplicar manifesto
kubectl delete deployment <nome>          # deletar deployment
kubectl scale deployment <nome> --replicas=3   # escalar
kubectl set image deployment/<nome> <container>=<nova-imagem>  # atualizar imagem
kubectl get deployment <nome> -o yaml     # ver manifesto atual completo
```

---

## 🔄 Rollout & Rollback

```bash
kubectl rollout status deployment/<nome>              # status do rollout
kubectl rollout history deployment/<nome>             # histórico de revisões
kubectl rollout history deployment/<nome> --revision=2  # detalhes de uma revisão
kubectl rollout undo deployment/<nome>                # voltar para versão anterior
kubectl rollout undo deployment/<nome> --to-revision=2  # voltar para revisão específica
kubectl rollout pause deployment/<nome>               # pausar rollout
kubectl rollout resume deployment/<nome>              # retomar rollout
```

---

## 📈 HPA — Autoscaler

```bash
kubectl autoscale deployment <nome> --min=2 --max=10 --cpu-percent=70
kubectl get hpa                           # listar HPAs
kubectl describe hpa <nome>              # detalhes + métricas atuais
kubectl delete hpa <nome>                # remover autoscaler
```

> ⚠️ Requer **metrics-server** instalado no cluster. No Minikube: `minikube addons enable metrics-server`

---

## 🏷 Namespaces

```bash
kubectl get namespaces                    # listar namespaces
kubectl create namespace <nome>           # criar namespace
kubectl delete namespace <nome>           # deletar namespace (apaga tudo dentro!)
kubectl config set-context --current --namespace=<nome>   # mudar namespace padrão
kubectl config view --minify | grep namespace  # ver namespace atual
kubectl get all -n <namespace>            # tudo dentro de um namespace
```

---

## 🌐 Networking — Services

```bash
kubectl get services                      # listar services
kubectl get svc                           # forma curta
kubectl describe service <nome>           # detalhes + endpoints
kubectl expose deployment <nome> --port=80 --type=ClusterIP   # criar service rápido
kubectl expose deployment <nome> --port=80 --type=NodePort
kubectl delete service <nome>
```

| Tipo | Quando usar |
|------|-------------|
| `ClusterIP` | Comunicação interna entre pods (padrão) |
| `NodePort` | Expor externamente via porta do nó (dev/lab) |
| `LoadBalancer` | Expor externamente em cloud (produção) |

---

## 🚦 Ingress

```bash
kubectl get ingress                       # listar ingresses
kubectl describe ingress <nome>           # detalhes + regras de roteamento
kubectl apply -f ingress.yaml             # aplicar manifesto
kubectl delete ingress <nome>             # remover ingress
```

> ⚠️ Requer **Ingress Controller** instalado. No Minikube: `minikube addons enable ingress`

**Como funciona:**
```
Internet → Ingress Controller → Ingress (regras) → Service → Pods
```

---

## ⚙️ ConfigMaps & Secrets

```bash
# ConfigMap
kubectl create configmap <nome> --from-literal=CHAVE=valor
kubectl create configmap <nome> --from-file=config.properties
kubectl get configmap
kubectl describe configmap <nome>
kubectl delete configmap <nome>

# Secret
kubectl create secret generic <nome> --from-literal=senha=minhasenha
kubectl create secret tls <nome> --cert=cert.pem --key=key.pem
kubectl get secrets
kubectl describe secret <nome>
kubectl delete secret <nome>

# Decodificar valor de um secret
kubectl get secret <nome> -o jsonpath='{.data.<chave>}' | base64 --decode
```

| | ConfigMap | Secret |
|---|---|---|
| Dados | Não sensíveis | Sensíveis (senhas, tokens, certs) |
| Encoding | Texto puro | Base64 |
| Uso | Env vars, arquivos de config | Env vars, volumes, TLS |

---

## 💾 Volumes, PV e PVC

```bash
kubectl get pv                            # listar PersistentVolumes
kubectl get pvc                           # listar PersistentVolumeClaims
kubectl describe pvc <nome>              # detalhes + status do binding
kubectl delete pvc <nome>                # remover claim
kubectl get storageclass                  # ver StorageClasses disponíveis
```

| Status PVC | Significado |
|---|---|
| `Pending` | Aguardando PV disponível |
| `Bound` | PVC vinculado a um PV |
| `Lost` | PV foi deletado |

| accessMode | Significado |
|---|---|
| `ReadWriteOnce` | Leitura/escrita por 1 nó |
| `ReadOnlyMany` | Somente leitura por vários nós |
| `ReadWriteMany` | Leitura/escrita por vários nós |

---

## 📦 Helm

```bash
# Repositórios
helm repo add <nome> <url>                # adicionar repositório
helm repo update                          # atualizar índice
helm search repo <termo>                  # buscar charts

# Releases
helm install <release> <chart>            # instalar
helm install <release> <chart> -f values.yaml          # com values customizados
helm install <release> <chart> --set chave=valor        # override pontual
helm upgrade <release> <chart>            # atualizar
helm upgrade --install <release> <chart>  # instala se não existir, atualiza se existir
helm rollback <release> <revisao>         # rollback
helm uninstall <release>                  # remover

# Inspeção
helm list                                 # listar releases
helm list -A                              # todos os namespaces
helm status <release>                     # status da release
helm get values <release>                 # values aplicados
helm show values <chart>                  # values padrão do chart
helm history <release>                    # histórico de revisões

# Criação de chart próprio
helm create <nome>                        # scaffold de um novo chart
helm lint <chart>                         # validar chart
helm template <release> <chart>           # renderizar templates sem instalar
helm package <chart>                      # empacotar em .tgz
```

---

## 📋 YAMLs Mínimos

> Copie, altere o que precisar e aplique com `kubectl apply -f arquivo.yaml`

### Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: meu-pod
  namespace: default
  labels:
    app: meu-app
spec:
  containers:
    - name: meu-container
      image: nginx:latest
      ports:
        - containerPort: 80
```

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: meu-deployment
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: meu-app
  template:
    metadata:
      labels:
        app: meu-app
    spec:
      containers:
        - name: meu-container
          image: nginx:latest
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "250m"
              memory: "256Mi"
```

### Service (ClusterIP)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: meu-service
  namespace: default
spec:
  selector:
    app: meu-app       # deve bater com o label do Deployment
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: meu-ingress
  namespace: default
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: meuapp.local          # altere para seu domínio
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: meu-service
                port:
                  number: 80
```

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: meu-configmap
  namespace: default
data:
  APP_ENV: production
  APP_PORT: "8080"
  config.properties: |
    chave1=valor1
    chave2=valor2
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: meu-secret
  namespace: default
type: Opaque
data:
  usuario: dXN1YXJpbw==      # base64 de "usuario"
  senha: c2VuaGEx             # base64 de "senha1"
  # Para gerar: echo -n "minha-senha" | base64
```

### PersistentVolumeClaim

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: meu-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: standard   # ajuste para o StorageClass do seu cluster
```

### HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: meu-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: meu-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

---

## 🔍 Troubleshooting Rápido

### Pod não sobe — checklist

```bash
kubectl get pods                          # ver status (Pending, CrashLoopBackOff, Error...)
kubectl describe pod <nome>              # olhar seção "Events" no final — causa real está aqui
kubectl logs <nome>                       # logs da aplicação
kubectl logs <nome> --previous            # logs do container que crashou antes de reiniciar
```

### Status comuns e o que significam

| Status | Provável causa |
|--------|----------------|
| `Pending` | Sem nó disponível, PVC não bound, resource insuficiente |
| `CrashLoopBackOff` | App subindo e crashando — ver `logs --previous` |
| `ImagePullBackOff` | Imagem não encontrada ou sem credencial de registry |
| `OOMKilled` | Container estourou o limite de memória |
| `Terminating` (preso) | Finalizer travado — `kubectl delete pod <nome> --force --grace-period=0` |
| `CreateContainerConfigError` | ConfigMap ou Secret referenciado não existe |

### Comandos de investigação

```bash
# Entrar no container para inspecionar
kubectl exec -it <pod> -- bash
kubectl exec -it <pod> -- sh                          # se não tiver bash

# Testar conectividade entre pods (requer curl/wget na imagem)
kubectl exec -it <pod> -- curl http://<service>:<porta>

# Ver eventos do cluster (últimos erros e avisos)
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Ver consumo de recursos
kubectl top pods                          # requer metrics-server
kubectl top nodes

# Ver em qual nó cada pod está rodando
kubectl get pods -o wide

# Inspecionar sem aplicar (dry-run)
kubectl apply -f arquivo.yaml --dry-run=client

# Ver diff antes de aplicar
kubectl diff -f arquivo.yaml
```

### Service não alcança os Pods

```bash
kubectl describe service <nome>           # verificar Endpoints — se vazio, selector não bate
kubectl get endpoints <nome>              # deve listar IPs dos pods
kubectl get pods --show-labels            # comparar labels com o selector do service
```

### Testar DNS interno do cluster

```bash
kubectl run debug --image=busybox --rm -it -- nslookup <service>.<namespace>.svc.cluster.local
```

---

## 🏴‍☠️ Flags Úteis

### `--dry-run=client -o yaml` — gerar YAML sem aplicar

```bash
# Ótimo ponto de partida para criar manifestos
kubectl create deployment meu-app --image=nginx --dry-run=client -o yaml > deployment.yaml
kubectl expose deployment meu-app --port=80 --dry-run=client -o yaml > service.yaml
kubectl create configmap meu-config --from-literal=ENV=prod --dry-run=client -o yaml
```

### `--watch` — monitorar em tempo real

```bash
kubectl get pods --watch                  # acompanhar mudanças de status ao vivo
kubectl get pods -w                       # forma curta
kubectl rollout status deployment/<nome>  # já faz watch até completar
```

### `--all-namespaces` / `-A` — ver tudo no cluster

```bash
kubectl get pods -A
kubectl get services -A
kubectl get ingress -A
kubectl get all -A
```

### `-o` — formatos de saída

```bash
kubectl get pod <nome> -o yaml            # manifesto YAML completo
kubectl get pod <nome> -o json            # em JSON
kubectl get pods -o wide                  # tabela com colunas extras (node, IP)
kubectl get pods -o name                  # só os nomes (útil em scripts)

# Extrair campo específico com jsonpath
kubectl get pod <nome> -o jsonpath='{.status.podIP}'
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
```

### Outras flags que salvam tempo

```bash
# Forçar delete de pod travado
kubectl delete pod <nome> --force --grace-period=0

# Aplicar todos os YAMLs de um diretório
kubectl apply -f ./manifests/

# Filtrar por label
kubectl get pods -l app=meu-app
kubectl get pods -l app=meu-app,env=prod

# Port-forward para testar localmente sem expor service
kubectl port-forward pod/<nome> 8080:80
kubectl port-forward service/<nome> 8080:80

# Ver pods de um namespace do sistema
kubectl get pods -n kube-system
```

---

## 📎 Referências

- [Documentação oficial do Kubernetes](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet oficial](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Helm Docs](https://helm.sh/docs/)
- [Artifact Hub](https://artifacthub.io/)
