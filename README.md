# 🚀 Kubernetes - Bruno Mori

> Referência de consulta rápida baseada nas aulas práticas do repositório.
> Comandos reais, YAMLs prontos para usar, troubleshooting e flags úteis.

---

## 📑 Índice

| # | Tema |
|---|------|
| 1 | [Docker — Comandos Base](#-docker--comandos-base) |
| 2 | [Pods](#-pods) |
| 3 | [ReplicaSets](#-replicasets) |
| 4 | [Deployments](#-deployments) |
| 5 | [Rollout & Rollback](#-rollout--rollback) |
| 6 | [HPA — Autoscaler](#-hpa--autoscaler) |
| 7 | [Namespaces](#-namespaces) |
| 8 | [Networking — Services](#-networking--services) |
| 9 | [Ingress](#-ingress) |
| 10 | [ConfigMaps & Secrets](#-configmaps--secrets) |
| 11 | [Volumes, PV e PVC](#-volumes-pv-e-pvc) |
| 12 | [Probes (Startup, Liveness, Readiness)](#-probes-startup-liveness-readiness) |
| 13 | [Helm](#-helm) |
| 14 | [YAMLs Mínimos](#-yamls-mínimos) |
| 15 | [Troubleshooting Rápido](#-troubleshooting-rápido) |
| 16 | [Flags Úteis](#-flags-úteis) |

---

## 🐳 Docker — Comandos Base

> Aula 1 — base antes do Kubernetes

```bash
docker build -t nome_da_imagem .          # build da imagem
docker images                             # listar imagens
docker run -d -p 8080:80 nome_da_imagem   # rodar container
docker ps                                 # containers rodando
docker ps -a                              # todos (parados também)
docker stop nome_da_imagem                # parar container
docker rm -f nome_da_imagem               # forçar remoção do container
docker rmi nome_da_imagem                 # remover imagem
```

---

## 🟢 Pods

> Aula 2 — menor unidade do Kubernetes. Pod ≠ Container. Não acessível externamente por padrão.

```bash
kubectl get nodes                         # verificar cluster funcionando
kubectl get pods                          # listar pods
kubectl get pods -o wide                  # com IP e nó
kubectl run nginx-run-pod --image=nginx   # criar pod rápido (imperativo)
kubectl get pod <nome> -o yaml            # ver YAML completo do pod
kubectl get pod <nome> -o yaml | grep -i ip   # pegar IP do pod
kubectl describe pod <nome>               # detalhes + eventos
kubectl logs <nome>                       # logs do pod
kubectl logs <nome> --previous            # logs do container que morreu
kubectl exec -it <nome> -- bash           # shell interativo
kubectl exec -it <nome> -- sh             # quando não tem bash
kubectl port-forward pod/<nome> 8080:80 --address=0.0.0.0  # expor localmente (DEBUG)
kubectl delete pod <nome>                 # deletar pod
```

> ⚠️ `port-forward` é **apenas para debug**. Não usar em produção.

---

## 🔁 ReplicaSets

> Aula 3 — garante que X Pods estejam sempre rodando. Auto-healing.

```bash
kubectl get rs                            # listar replicasets
kubectl get rs -w                         # monitorar em tempo real
kubectl describe replicaset <nome>        # detalhes + eventos
kubectl apply -f my-app-rs.yaml           # criar replicaset via YAML
kubectl scale rs <nome> --replicas=5      # escalar manualmente
kubectl scale rs <nome> --replicas=0      # desligar todos os pods
kubectl delete rs <nome>                  # deletar (remove pods junto)
```

> ⚠️ Em produção **não use ReplicaSet direto**. Use Deployment.

---

## 🚀 Deployments

> Aula 4 — padrão de produção. Hierarquia: **Deployment → ReplicaSet → Pods**

```bash
# Gerar YAML sem aplicar (boa prática para criar manifestos)
kubectl create deployment my-nginx-app \
  --image=nginx:1.14.2 \
  --replicas=3 \
  --dry-run=client -o yaml > my-nginx-deployment.yaml

kubectl apply -f my-nginx-deployment.yaml         # aplicar
kubectl get deployments                           # listar
kubectl get deployment <nome> -o wide             # com imagem e seletores
kubectl describe deployment <nome>                # detalhes + eventos
kubectl rollout status deployment/<nome>          # acompanhar status
kubectl rollout restart deployment/<nome>         # recriar pods sem downtime
kubectl scale deployment <nome> --replicas=3      # escalar
kubectl set image deployment/<nome> <container>=<nova-imagem>  # atualizar imagem
kubectl delete deployment <nome>                  # deletar
```

> 💡 `rollout restart` recria os Pods mantendo a mesma imagem — útil para forçar reload de ConfigMaps/Secrets.

---

## 🔄 Rollout & Rollback

> Aula 4.1 / 4.2 — simular falha, auditar histórico e reverter com segurança

```bash
kubectl rollout status deployment/<nome>              # status atual
kubectl rollout history deployment/<nome>             # histórico de revisões
kubectl rollout history deployment/<nome> --revision=2  # detalhes de uma revisão

# Simular falha (imagem inexistente)
kubectl set image deployment/<nome> nginx=nginx:inexistente

# Anotar motivo da mudança (boa prática de auditoria)
kubectl annotate deployment/<nome> \
  kubernetes.io/change-cause="Deploy Failure - versão inexistente"

# Rollback
kubectl rollout undo deployment/<nome>                # voltar para revisão anterior
kubectl rollout undo deployment/<nome> --to-revision=1  # revisão específica

kubectl rollout pause deployment/<nome>               # pausar rollout
kubectl rollout resume deployment/<nome>              # retomar rollout
```

> 💡 Ao fazer rollback, o Kubernetes **cria uma nova revisão** — não apaga o histórico.

---

## 📈 HPA — Autoscaler

> Aula 4.3 — escalabilidade horizontal baseada em CPU

```bash
kubectl autoscale deployment <nome> --min=2 --max=10 --cpu-percent=70
kubectl get hpa                           # listar HPAs
kubectl describe hpa <nome>              # detalhes + métricas atuais
kubectl delete hpa <nome>                # remover autoscaler
```

> ⚠️ Requer **metrics-server** no cluster.
> Minikube: `minikube addons enable metrics-server`

---

## 🏷 Namespaces

> Aula 5 — isolamento lógico de recursos

```bash
kubectl get namespaces                    # listar namespaces
kubectl create namespace <nome>           # criar namespace
kubectl create ns <nome>                  # forma curta
kubectl delete namespace <nome>           # deletar (apaga tudo dentro!)
kubectl get all -n <namespace>            # tudo dentro de um namespace
kubectl config set-context --current --namespace=<nome>   # mudar namespace padrão
kubectl config view --minify | grep namespace  # ver namespace atual
```

> 💡 Padrão no curso: namespace `config-e-persist` para as aulas 8 e 9.

---

## 🌐 Networking — Services

> Aula 6 — como expor aplicações dentro e fora do cluster

```bash
kubectl get services                      # listar services
kubectl get svc                           # forma curta
kubectl get svc -n <namespace>
kubectl describe service <nome>           # detalhes + endpoints
kubectl expose deployment <nome> --port=80 --type=ClusterIP
kubectl expose deployment <nome> --port=80 --type=NodePort
kubectl get endpoints <nome>             # ver IPs dos pods vinculados
kubectl delete service <nome>
```

| Tipo | Quando usar |
|------|-------------|
| `ClusterIP` | Comunicação interna entre pods (padrão) |
| `NodePort` | Expor externamente via porta do nó (dev/lab) |
| `LoadBalancer` | Expor externamente em cloud (produção) |

---

## 🚦 Ingress

> Aula 7 — roteamento HTTP externo para serviços internos

```bash
# Habilitar no Minikube
minikube addons enable ingress

# Verificar Ingress Controller
kubectl get ingressclass
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx

kubectl get ingress                       # listar ingresses
kubectl get ingress -n <namespace>
kubectl describe ingress <nome>           # regras de roteamento + eventos
kubectl apply -f ingress.yaml
kubectl delete ingress <nome>
```

**Fluxo real:**
```
Client → DNS → Ingress Controller → Ingress (regras) → Service → Endpoint → Pod
```

| Erro | Causa provável |
|------|----------------|
| `ADDRESS` vazio | externalIP/LoadBalancer não configurado |
| `404 Not Found` | namespace errado, service não existe, selector incorreto |
| `503 Service Unavailable` | sem endpoints — pod não sendo selecionado pelo service |

---

## ⚙️ ConfigMaps & Secrets

> Aula 8 — configuração separada da imagem. Padrão obrigatório em produção.

```bash
# ConfigMap
kubectl create configmap <nome> --from-literal=DATABASE_URL="jdbc:mysql://..." -n <ns>
kubectl create configmap <nome> --from-file=config.properties
kubectl get configmap -n <namespace>
kubectl describe cm <nome> -n <namespace>

# Secret
kubectl create secret generic <nome> \
  --from-literal=USERNAME='usuario' \
  --from-literal=PASSWORD='senha' \
  -n <namespace>
kubectl create secret tls <nome> --cert=cert.pem --key=key.pem
kubectl get secrets -n <namespace>
kubectl describe secret <nome> -n <namespace>
kubectl get secret <nome> -o yaml -n <namespace>   # ver dados em base64

# Decodificar valor de um secret
kubectl get secret <nome> -o jsonpath='{.data.<chave>}' | base64 --decode

# Gerar base64 para colocar no YAML
echo -n "minha-senha" | base64
```

| | ConfigMap | Secret |
|---|---|---|
| Dados | Não sensíveis | Sensíveis (senhas, tokens, certs) |
| Encoding | Texto puro | Base64 |
| Injetar via | `configMapRef` / volume | `secretRef` / volume |

> 💡 Usar `envFrom` com `configMapRef` e `secretRef` injeta **todas as chaves** como variáveis de ambiente.

---

## 💾 Volumes, PV e PVC

> Aula 8.1 — persistência de dados além do ciclo de vida do Pod

```bash
kubectl get pv                            # PersistentVolumes (cluster-wide)
kubectl get pvc -n <namespace>            # PersistentVolumeClaims
kubectl describe pvc <nome> -n <ns>       # status do binding
kubectl get storageclass                  # StorageClasses disponíveis
kubectl delete pvc <nome> -n <ns>
kubectl delete pv <nome>
```

**Fluxo de persistência:**
```
Container (efêmero)
      ↓
Volume Mount (mountPath no pod)
      ↓
PVC (pedido de armazenamento)
      ↓
PV (volume real)
      ↓
Disco do Node / Storage
```

| Status PVC | Significado |
|---|---|
| `Pending` | Aguardando PV disponível |
| `Bound` | Vinculado a um PV — pronto para uso |
| `Lost` | PV foi deletado |

| accessMode | Significado |
|---|---|
| `ReadWriteOnce` | Leitura/escrita por 1 nó |
| `ReadOnlyMany` | Somente leitura por vários nós |
| `ReadWriteMany` | Leitura/escrita por vários nós |

> 💡 Mesmo deletando o Deployment, os dados persistem no PV enquanto o PVC existir.

---

## 🩺 Probes (Startup, Liveness, Readiness)

> Aula 9 — habilidade obrigatória para SRE. Detecta falhas automaticamente.

```bash
# Monitorar comportamento das probes
kubectl get pods -n <namespace> -w
kubectl describe pod <nome> -n <ns>       # seção Events mostra falhas de probe
kubectl logs <nome> -n <ns> -f            # logs em tempo real

# Simular falha de Liveness
kubectl edit deployment my-app -n <ns>    # alterar HEALTH_STATUS_OK=false

# Simular falha de Readiness (desligar banco)
kubectl scale deployment mysql --replicas=0 -n <ns>
# Resultado: pod fica Running mas Ready 0/1
kubectl scale deployment mysql --replicas=1 -n <ns>   # religar
```

| Probe | O que verifica | Se falhar |
|---|---|---|
| `StartupProbe` | Aplicação terminou de iniciar | Reinicia o container |
| `LivenessProbe` | Aplicação continua saudável | Reinicia o container |
| `ReadinessProbe` | Pode receber tráfego (ex: banco conectado) | Remove do Service — **não reinicia** |

> ⚠️ `ReadinessProbe` falhando → usuário recebe `503 Service Unavailable` mas o pod não é reiniciado.

---

## 📦 Helm

> Aula 10 — gerenciador de pacotes do Kubernetes

```bash
# Instalação
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version

# Repositórios
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo nginx

# Deploy — forma real usada em SRE
helm upgrade --install meu-nginx bitnami/nginx           # cria ou atualiza
helm upgrade --install meu-nginx bitnami/nginx --atomic  # com rollback automático se falhar
helm upgrade --install meu-nginx bitnami/nginx -n dev --create-namespace

# Customizar com values
helm show values bitnami/nginx > values.yaml             # exportar values padrão
helm upgrade --install meu-nginx bitnami/nginx -f values.yaml
helm upgrade --install meu-nginx bitnami/nginx --set service.type=NodePort

# Debug
helm status meu-nginx
helm get values meu-nginx
helm install meu-nginx bitnami/nginx --dry-run --debug   # simular sem aplicar

# Histórico e rollback
helm history meu-nginx
helm rollback meu-nginx 1                                # voltar para revisão 1

# Limpeza
helm uninstall meu-nginx
helm list
helm list -A                                             # todos os namespaces
```

> 💡 `helm upgrade --install` é o comando padrão em pipelines CI/CD — funciona tanto para criar quanto para atualizar.

---

## 📋 YAMLs Mínimos

> Copie, ajuste os campos marcados e aplique com `kubectl apply -f arquivo.yaml`

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
  name: my-nginx-app
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-nginx-app
  template:
    metadata:
      labels:
        app: my-nginx-app
    spec:
      containers:
        - name: nginx
          image: nginx:1.14.2       # altere a versão aqui
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
    app: my-nginx-app               # deve bater com o label do Deployment
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP
```

### Ingress (NGINX)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-pay
  namespace: ecommerce              # ajuste o namespace
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: my-kubernetes.com.br    # altere para seu domínio / /etc/hosts
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
  name: app-config
  namespace: config-e-persist
data:
  DATABASE_URL: "jdbc:mysql://mysql.config-e-persist.svc.cluster.local:3306/testdb"
  APP_ENV: production
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: config-e-persist
type: Opaque
data:
  USERNAME: dXNlcm5hbWU=           # base64 de "username" → echo -n "username" | base64
  PASSWORD: cGFzc3dvcmQ=           # base64 de "password"
```

### PersistentVolumeClaim

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
  namespace: config-e-persist
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: local-path      # ajuste para o StorageClass do cluster
  resources:
    requests:
      storage: 1Gi
```

### Deployment com Probes completas

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: config-e-persist
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
          image: minha-imagem:tag
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
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            failureThreshold: 3
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: db-credentials
          volumeMounts:
            - name: meu-storage
              mountPath: /var/lib/dados
      volumes:
        - name: meu-storage
          persistentVolumeClaim:
            claimName: mysql-pvc
```

### HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: meu-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-nginx-app
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

### Checklist — Pod não sobe

```bash
kubectl get pods -n <ns>                  # ver status
kubectl describe pod <nome> -n <ns>       # seção "Events" no final — causa real está aqui
kubectl logs <nome> -n <ns>               # logs da aplicação
kubectl logs <nome> -n <ns> --previous    # logs do container que crashou
```

### Status comuns e causas

| Status | Provável causa |
|--------|----------------|
| `Pending` | Sem nó disponível, PVC não bound, resource insuficiente |
| `CrashLoopBackOff` | App subindo e crashando — ver `logs --previous` |
| `ImagePullBackOff` | Imagem não encontrada ou sem credencial de registry |
| `OOMKilled` | Container estourou limite de memória |
| `CreateContainerConfigError` | ConfigMap ou Secret referenciado não existe |
| `Terminating` (preso) | Finalizer travado → `kubectl delete pod <nome> --force --grace-period=0` |
| `Running` mas `Ready 0/1` | ReadinessProbe falhando (ex: banco fora) |

### Service não alcança os Pods

```bash
kubectl describe service <nome> -n <ns>   # verificar Endpoints — se vazio, selector não bate
kubectl get endpoints <nome> -n <ns>      # deve listar IPs dos pods
kubectl get pods --show-labels -n <ns>    # comparar labels com selector do service
```

### Investigação geral

```bash
# Eventos do cluster (últimos erros)
kubectl get events --sort-by='.lastTimestamp' -n <ns>

# Entrar no container
kubectl exec -it <pod> -n <ns> -- bash

# Testar DNS interno
kubectl run debug --image=busybox --rm -it -- \
  nslookup mysql.config-e-persist.svc.cluster.local

# Testar conectividade entre pods
kubectl exec -it <pod> -n <ns> -- curl http://<service>:<porta>

# Ver consumo de recursos
kubectl top pods -n <ns>
kubectl top nodes

# Ver diff antes de aplicar
kubectl diff -f arquivo.yaml
```

---

## 🏴‍☠️ Flags Úteis

### `--dry-run=client -o yaml` — gerar YAML sem criar nada

```bash
kubectl create deployment my-app --image=nginx --dry-run=client -o yaml > deployment.yaml
kubectl expose deployment my-app --port=80 --dry-run=client -o yaml > service.yaml
kubectl create configmap app-config --from-literal=ENV=prod --dry-run=client -o yaml
```

### `--watch` / `-w` — monitorar em tempo real

```bash
kubectl get pods -w
kubectl get rs -w
kubectl rollout status deployment/<nome>  # já faz watch até completar
```

### `-A` / `--all-namespaces` — ver tudo no cluster

```bash
kubectl get pods -A
kubectl get svc -A
kubectl get ingress -A
kubectl get all -A
```

### `-o` — formatos de saída

```bash
kubectl get pod <nome> -o yaml
kubectl get pod <nome> -o json
kubectl get pods -o wide                  # tabela com node e IP
kubectl get pods -o name                  # só nomes (útil em scripts)

# Extrair campos específicos
kubectl get pod <nome> -o jsonpath='{.status.podIP}'
kubectl get secret <nome> -o jsonpath='{.data.PASSWORD}' | base64 --decode
```

### Outras flags que salvam tempo

```bash
# Forçar delete de pod travado
kubectl delete pod <nome> --force --grace-period=0

# Aplicar todos os YAMLs de um diretório
kubectl apply -f ./manifests/

# Filtrar por label
kubectl get pods -l app=my-app
kubectl get pods -l app=my-app,env=prod

# Port-forward para testar localmente
kubectl port-forward pod/<nome> 8080:80
kubectl port-forward service/<nome> 8080:80

# Anotar deployment (auditoria de mudanças)
kubectl annotate deployment/<nome> kubernetes.io/change-cause="Deploy v2.0 - nova feature X"
```

---

## 📎 Referências

- [Documentação oficial do Kubernetes](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet oficial](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Helm Docs](https://helm.sh/docs/)
- [Artifact Hub](https://artifacthub.io/)
- [Repositório das Aulas — Bruno Mori](https://github.com/brunomori/Exercicio-Kubernets-)
