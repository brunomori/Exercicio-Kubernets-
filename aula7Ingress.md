markdown
# 🚦 Guia Prático: Ingress no Kubernetes (Com Nginx)

Este guia cobre desde a instalação do **Ingress Controller** até a criação do seu primeiro Ingress, com foco em colocar a mão na massa.

## 📌 Índice
1. [O que é Ingress? (Teoria Rápida)](#o-que-é-ingress-teoria-rápida)
2. [Pré-requisitos](#pré-requisitos)
3. [Passo 1: Instalar o Nginx Ingress Controller](#passo-1-instalar-o-nginx-ingress-controller)
4. [Passo 2: Setup das Aplicações (Deployments & Services)](#passo-2-setup-das-aplicações-deployments--services)
5. [Passo 3: Criar um Ingress Simples (Backend Único)](#passo-3-criar-um-ingress-simples-backend-único)
6. [🧪 Exercício Prático](#-exercício-prático)

---

## O que é Ingress? (Teoria Rápida)

Imagine que você tem várias lojinhas (os **Services** do Kubernetes) dentro de um mesmo shopping (seu cluster). O **Ingress** é como a **porta principal e a placa de sinalização** desse shopping. Em vez de você ter que lembrar o número de cada loja (ou IP de cada serviço), você entra pela porta principal e a placa te direciona: "Pagamentos é no corredor A, Vídeos no corredor B".

- **Função:** Gerenciar o **acesso externo** (HTTP/HTTPS) aos serviços dentro do cluster.
- **Regras:** Define como o tráfego deve ser roteado baseado no **host** (ex: `my-kubernetes.com.br`) ou no **caminho** da URL (ex: `/pay`, `/video`).
- **Ingress Controller:** O Ingress é só uma regra (um objeto de configuração). Quem **executa** essa regra é o **Ingress Controller** (como o Nginx, Traefik, HAProxy). Ele é o "segurança" que lê a placa e direciona o cliente para a loja certa.
    - Existem vários controllers (NGINX, Traefik, Contour, etc.). Neste guia, usaremos o **NGINX Ingress Controller**.

---

## Pré-requisitos

- Um cluster Kubernetes rodando.
- Acesso ao `kubectl` configurado.
- Uma VM com IP acessível (para simular um IP público). Neste exemplo, usaremos `192.168.0.32`.

---

## Passo 1: Instalar o Nginx Ingress Controller

Vamos implantar o controller que vai "ler" e aplicar as regras dos nossos Ingresses.

### 1.1. Criar pasta para os manifestos
```bash
mkdir -p /root/aplicacoes/ingress
1.2. Fazer o download do manifesto de instalação
bash
curl -L \
https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/baremetal/deploy.yaml \
-o /root/aplicacoes/ingress/nginx-ingress-controller-deploy.yaml
Nota: Usei -L para seguir redirecionamentos e -o para salvar o arquivo.

1.3. ⚙️ CORREÇÃO IMPORTANTE: Configurar o IP Externo
Para acessar o Ingress de fora do cluster (no seu navegador, por exemplo), precisamos atribuir um externalIP ao serviço do controller.

Edite o arquivo baixado:

bash
vim /root/aplicacoes/ingress/nginx-ingress-controller-deploy.yaml
Procure pelo Service chamado ingress-nginx-controller no namespace ingress-nginx. Adicione as linhas externalIPs conforme abaixo:

yaml
apiVersion: v1
kind: Service
metadata:
  name: ingress-nginx-controller
  namespace: ingress-nginx
spec:
  type: NodePort
  externalIPs:   # <--- ADICIONE ESTA LINHA
  - 192.168.0.32 # <--- ADICIONE ESTA LINHA (com o IP da sua VM)
  # ... o resto da configuração continua igual
1.4. Implantar o Controller
bash
k create -f /root/aplicacoes/ingress/nginx-ingress-controller-deploy.yaml
1.5. Verificar a instalação
bash
k get all -n ingress-nginx
Aguarde até que todos os pods estejam com o status Running.

1.6. Configurar o DNS local (arquivo hosts)
Para o nome my-kubernetes.com.br apontar para o seu cluster, adicione a seguinte linha ao arquivo de hosts da sua máquina LOCAL (não a VM, mas o seu computador).

Linux/Mac: /etc/hosts

Windows: C:\Windows\System32\drivers\etc\hosts

hosts
192.168.0.32        my-kubernetes.com.br
Passo 2: Setup das Aplicações (Deployments & Services)
Vamos criar as "lojinhas" (aplicações) que serão expostas pelo Ingress.

2.1. Criar a pasta de setup
bash
mkdir -p /root/aplicacoes/ingress/setup-ecommerce
2.2. Criar o manifesto com Deployments e Services
Este manifesto cria o namespace ecommerce e 4 aplicações (food, video, pay, apparels) com seus respectivos Services.

bash
cat > /root/aplicacoes/ingress/setup-ecommerce/setup-ecommerce.yaml <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: food
    tier: frontend
  name: food
  namespace: ecommerce
spec:
  replicas: 1
  selector:
    matchLabels:
      app: food
  template:
    metadata:
      labels:
        app: food
    spec:
      containers:
      - image: bsllacerda/ecommerce:food
        name: food
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: video
    tier: frontend
  name: video
  namespace: ecommerce
spec:
  replicas: 1
  selector:
    matchLabels:
      app: video
  template:
    metadata:
      labels:
        app: video
    spec:
      containers:
      - image: bsllacerda/ecommerce:video
        name: video
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: pay
    tier: frontend
  name: pay
  namespace: ecommerce
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pay
  template:
    metadata:
      labels:
        app: pay
    spec:
      containers:
      - image: bsllacerda/ecommerce:pay
        name: pay
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: apparels
    tier: frontend
  name: apparels
  namespace: ecommerce
spec:
  replicas: 1
  selector:
    matchLabels:
      app: apparels
  template:
    metadata:
      labels:
        app: apparels
    spec:
      containers:
      - image: bsllacerda/ecommerce:apparels
        name: apparels
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: food
  name: food
  namespace: ecommerce
spec:
  ports:
  - port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    app: food
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: video
  name: video
  namespace: ecommerce
spec:
  ports:
  - port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    app: video
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: pay
  name: pay
  namespace: ecommerce
spec:
  ports:
  - port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    app: pay
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: apparels
  name: apparels
  namespace: ecommerce
spec:
  ports:
  - port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    app: apparels
EOF
2.3. Aplicar o manifesto
bash
k apply -f /root/aplicacoes/ingress/setup-ecommerce/setup-ecommerce.yaml
2.4. Verificar a criação
bash
# Verifique os Pods
k get pods -n ecommerce

# Verifique os Services
k get svc -n ecommerce
Todos os pods devem estar Running e os services criados.

Passo 3: Criar um Ingress Simples (Backend Único)
Agora vamos criar uma regra de Ingress que vai direcionar TODO o tráfego que chegar em my-kubernetes.com.br para o serviço pay.

3.1. Criar o manifesto do Ingress
bash
cat > /root/aplicacoes/ingress/setup-ecommerce/ing-backed-single-service.yaml <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: backed-by-a-single-service
  labels:
    type: backed-by-a-single-service
  namespace: ecommerce
spec:
  ingressClassName: nginx
  defaultBackend:
    service:
      name: pay
      port:
        number: 8080
EOF
Entendendo o manifesto:

ingressClassName: nginx: Diz para o Kubernetes usar o controller do Nginx que instalamos.

defaultBackend: É um back-end padrão. Como não definimos nenhuma rule (regra de host ou caminho), qualquer requisição que chegar neste IP/nome será enviada para o serviço pay na porta 8080.

3.2. Aplicar o Ingress
bash
k apply -f /root/aplicacoes/ingress/setup-ecommerce/ing-backed-single-service.yaml
3.3. Verificar o Ingress
bash
# Verifique o status e o IP (pode levar alguns segundos/minutos)
k get ing -n ecommerce -w
Quando o IP for atribuído, você verá algo como:

text
NAME                         CLASS   HOSTS   ADDRESS        PORTS   AGE
backed-by-a-single-service   nginx   *       192.168.0.32   80      10s
3.4. Descrever o Ingress para mais detalhes
bash
k describe ing -n ecommerce backed-by-a-single-service
Na seção Default backend, você verá o serviço pay:8080.

3.5. Testar no navegador
Acesse: http://my-kubernetes.com.br

Se tudo deu certo, você verá a página da aplicação "pay" (provavelmente algo relacionado a pagamentos).

🧪 Exercício Prático
Objetivo: Modificar o Ingress existente para que ele exponha um serviço diferente.

Altere o manifesto do Ingress (ing-backed-single-service.yaml) para que o defaultBackend aponte para o serviço video na porta 8080.

Aplique a alteração com o comando k apply -f ....

Teste novamente o endereço http://my-kubernetes.com.br. A página que aparece agora é da aplicação de vídeos?

(Opcional) Use o comando k edit ing -n ecommerce backed-by-a-single-service para fazer a mesma alteração "ao vivo" no cluster, sem editar o arquivo YAML.

Com esse exercício, você viu como é fácil trocar o "back-end" que está sendo exposto pelo Ingress. Na próxima aula, você verá como expor múltiplos serviços ao mesmo tempo (Fanout).

text

---

Para baixar:

1. **Clique com o botão direito** [neste link](sandbox:/mnt/data/ingress-kubernetes-guia.md)
2. **Escolha "Salvar link como..."** ou **"Save link as..."**
3. **Salve** o arquivo como `ingress-kubernetes-guia.md`

Ou copie todo o conteúdo acima, cole em um bloco de notas e salve com a extensão `.md`
