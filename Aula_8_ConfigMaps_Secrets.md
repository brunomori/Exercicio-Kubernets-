# 🔐 Kubernetes c --- Guia Prático 

Guia prático para aprender **ConfigMaps e Secrets no Kubernetes** usando
uma aplicação real que conecta em um **banco MySQL**.

Este material é focado em **prática real de ambiente DevOps / SRE**.

------------------------------------------------------------------------

# 🎯 Objetivo da Aula

Ao final deste exercício você será capaz de:

-   Criar **Namespaces**
-   Criar **ConfigMaps**
-   Criar **Secrets**
-   Injetar configurações em containers
-   Verificar variáveis de ambiente dentro de Pods
-   Expor aplicações com **Service**
-   Acessar aplicações com **Ingress**

------------------------------------------------------------------------

# 🧠 Conceito Importante

Em Kubernetes **configuração nunca deve ficar dentro da imagem da
aplicação**.

Separação correta:

  Tipo         Usado para
  ------------ -----------------------------
  ConfigMap    Configurações não sensíveis
  Secret       Senhas, tokens, chaves
  Deployment   Aplicação
  Service      Exposição interna
  Ingress      Exposição externa

------------------------------------------------------------------------

# 🏗 Arquitetura da Aula

Fluxo da aplicação:

    ConfigMap ----\
                   ---> Deployment ---> Pod ---> Aplicação
    Secret    ----/

    Service  ---> acesso interno
    Ingress  ---> acesso via navegador

------------------------------------------------------------------------

# 📦 1 --- Criando Namespace

Namespaces isolam recursos dentro do cluster.

``` bash
kubectl create ns config-e-persist
```

Verificar:

``` bash
kubectl get ns
```

------------------------------------------------------------------------

# 🗂 2 --- Criando ConfigMap

O ConfigMap armazenará a **URL de conexão do banco**.

``` bash
kubectl create configmap app-config --from-literal=DATABASE_URL="jdbc:mysql://mysql.config-e-persist.svc.cluster.local:3306/testdb" -n config-e-persist
```

Verificar:

``` bash
kubectl -n config-e-persist get configmap
```

Detalhes:

``` bash
kubectl -n config-e-persist describe cm app-config
```

------------------------------------------------------------------------

# 🔑 3 --- Criando Secret

Secrets armazenam **dados sensíveis**.

Exemplo:

-   usuário
-   senha

``` bash
kubectl create secret generic db-credentials --from-literal=USERNAME='username' --from-literal=PASSWORD='password' -n config-e-persist
```

Verificar:

``` bash
kubectl -n config-e-persist get secret
```

Detalhes:

``` bash
kubectl -n config-e-persist describe secret db-credentials
```

Ver YAML:

``` bash
kubectl -n config-e-persist get secret db-credentials -o yaml
```

⚠️ Secrets aparecem codificados em **Base64**.

------------------------------------------------------------------------

# 🚀 4 --- Deploy da Aplicação

Criar **Service, Ingress e Deployment**.

``` bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: my-app
  namespace: config-e-persist
spec:
  type: ClusterIP
  selector:
    app: my-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app
  namespace: config-e-persist
  annotations:
    nginx.ingress.kubernetes.io/use-regex: "true"
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  ingressClassName: nginx
  rules:
  - host: my-kubernetes.com.br
    http:
      paths:
      - pathType: ImplementationSpecific
        path: /my-app(/|$)(.*)
        backend:
          service:
            name: my-app
            port:
              number: 80
---
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
        image: bsllacerda/quarkus-examples:quarkus-mysql-connection@sha256:618bc24074f51182a03f8cf37a40af95416bd1016597a04d8f9cba89154a2d17
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: db-credentials
EOF
```

------------------------------------------------------------------------

# 🔎 5 --- Verificando Recursos

Pods:

``` bash
kubectl -n config-e-persist get pods
```

Services:

``` bash
kubectl -n config-e-persist get svc
```

Ingress:

``` bash
kubectl -n config-e-persist get ingress
```

------------------------------------------------------------------------

# 🧪 6 --- Verificando Variáveis no Container

Entrar no Pod:

``` bash
kubectl -n config-e-persist exec -it NOME_DO_POD -- /bin/bash
```

Listar variáveis:

``` bash
env
```

Filtrar apenas as relevantes:

``` bash
env | grep -E "DATABASE|USERNAME|PASSWORD"
```

Saída esperada:

    DATABASE_URL=jdbc:mysql://...
    USERNAME=username
    PASSWORD=password

------------------------------------------------------------------------

# 🌐 7 --- Testando a Aplicação

Abrir no navegador:

    https://my-kubernetes.com.br/my-app

------------------------------------------------------------------------

# 📜 Logs da Aplicação

Logs ajudam a identificar erros de:

-   conexão com banco
-   variáveis incorretas
-   falha de startup

``` bash
kubectl -n config-e-persist logs NOME_DO_POD
```

------------------------------------------------------------------------

# 🧹 Limpando o Ambiente

``` bash
kubectl -n config-e-persist delete ingress my-app
kubectl -n config-e-persist delete svc my-app
kubectl -n config-e-persist delete deployment my-app
kubectl -n config-e-persist delete cm app-config
kubectl -n config-e-persist delete secret db-credentials
kubectl delete ns config-e-persist
```

------------------------------------------------------------------------

# 🧠 Mentalidade SRE

Separar configuração da aplicação permite:

-   mudar configs **sem rebuild da imagem**
-   usar **GitOps**
-   ter **ambientes diferentes (dev/staging/prod)**
-   melhorar **segurança de credenciais**

Esse padrão é **usado em praticamente todos clusters Kubernetes em
produção**.

------------------------------------------------------------------------

# 🧪 Exercício de Fixação

1️⃣ Crie um novo ConfigMap

    APP_ENV=production
    APP_VERSION=1.0

2️⃣ Crie um Secret

    API_KEY=123456

3️⃣ Injete no Deployment usando:

    envFrom

4️⃣ Verifique dentro do Pod

``` bash
env | grep APP
```

------------------------------------------------------------------------

# 📚 Comandos Kubernetes Utilizados

  Comando                    Função
  -------------------------- ------------------------------
  kubectl create ns          cria namespace
  kubectl create configmap   cria ConfigMap
  kubectl create secret      cria Secret
  kubectl apply              cria recursos via YAML
  kubectl get                lista recursos
  kubectl describe           detalhes
  kubectl exec               executa comando no container
  kubectl logs               logs da aplicação

------------------------------------------------------------------------

✅ Agora você domina **ConfigMaps e Secrets no Kubernetes**, um dos
fundamentos mais importantes para **DevOps e SRE**.
