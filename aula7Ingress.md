# 🚦 Guia Prático: Ingress no Kubernetes com NGINX

Este guia cobre desde a instalação do **Ingress Controller** até a
criação do seu primeiro recurso de **Ingress**, com foco total em
prática.

------------------------------------------------------------------------

## 📌 Índice

1.  O que é Ingress?
2.  Pré-requisitos
3.  Passo 1: Instalar o NGINX Ingress Controller
4.  Passo 2: Criar as Aplicações (Deployments & Services)
5.  Passo 3: Criar um Ingress Simples
6.  Teste e Validação
7.  Exercício Prático

------------------------------------------------------------------------

# O que é Ingress?

O **Ingress** funciona como uma porta principal inteligente que:

-   Recebe tráfego HTTP/HTTPS externo
-   Analisa host ou caminho da URL
-   Direciona para o Service correto

Sem um Ingress Controller instalado, o recurso Ingress não funciona.

------------------------------------------------------------------------

# Pré-requisitos

-   Cluster Kubernetes funcionando
-   kubectl configurado
-   Acesso root (ou sudo)
-   IP da máquina acessível (exemplo: 192.168.0.32)

------------------------------------------------------------------------

# Passo 1: Instalar o NGINX Ingress Controller

## Criar diretório

``` bash
sudo mkdir -p /root/aplicacoes/ingress
```

## Baixar manifesto

``` bash
curl -L https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/baremetal/deploy.yaml -o /root/aplicacoes/ingress/nginx-ingress-controller.yaml
```

## Ajustar externalIPs

Edite o Service ingress-nginx-controller:

``` yaml
spec:
  type: NodePort
  externalIPs:
  - 192.168.0.32
```

## Aplicar

``` bash
kubectl apply -f /root/aplicacoes/ingress/nginx-ingress-controller.yaml
```

## Validar

``` bash
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
```

------------------------------------------------------------------------

# Configurar DNS Local

Adicionar no /etc/hosts ou no arquivo hosts do Windows:

    192.168.0.32   my-kubernetes.com.br

------------------------------------------------------------------------

# Passo 2: Criar Aplicações

## Criar diretório

``` bash
sudo mkdir -p /root/aplicacoes/ingress/ecommerce
```

## Aplicar manifesto ecommerce.yaml

``` bash
kubectl apply -f /root/aplicacoes/ingress/ecommerce/ecommerce.yaml
```

## Validar

``` bash
kubectl get pods -n ecommerce
kubectl get svc -n ecommerce
```

------------------------------------------------------------------------

# Passo 3: Criar Ingress

## Criar arquivo ingress-pay.yaml

``` yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-pay
  namespace: ecommerce
spec:
  ingressClassName: nginx
  defaultBackend:
    service:
      name: pay
      port:
        number: 8080
```

## Aplicar

``` bash
kubectl apply -f ingress-pay.yaml
```

## Verificar

``` bash
kubectl get ingress -n ecommerce -w
```

## Descrever

``` bash
kubectl describe ingress ingress-pay -n ecommerce
```

------------------------------------------------------------------------

# Teste

Acesse no navegador:

http://my-kubernetes.com.br

------------------------------------------------------------------------

# Exercício Prático

1.  Alterar o Ingress para apontar para o serviço video.
2.  Aplicar novamente.
3.  Testar no navegador.
4.  Opcional: usar kubectl edit ingress.
