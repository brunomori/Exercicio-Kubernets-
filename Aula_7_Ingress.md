# 🚦 Ingress no Kubernetes -- Guia Prático (Versão SRE Jr)

Guia direto ao ponto para entender, instalar e operar Ingress com
mentalidade de SRE.

------------------------------------------------------------------------

# 🎯 Objetivo

Ao final deste guia você será capaz de:
a
-   Entender o fluxo real de uma requisição HTTP no cluster
-   Instalar o NGINX Ingress Controlleraa
-   Expor aplicações externamente
-   Diagnosticar erros comuns (404, 503, ADDRESS vazio)

------------------------------------------------------------------------

# 🧠 Conceito Técnico (Sem Metáfora)

Fluxo real de requisição:

Client → DNS → Ingress Controller → Service → Endpoint → Pod

## Diferença Importante

-   **Ingress** → Recurso de configuração (regras)
-   **Ingress Controller** → Implementação que executa as regras
-   **Sem controller, Ingress não funciona**

Verifique controllers disponíveis:

``` bash
kubectl get ingressclass
```

------------------------------------------------------------------------

# 📋 Pré-requisitos

-   Cluster Kubernetes funcionando
-   kubectl configurado
-   IP acessível (exemplo: 192.168.0.32)

------------------------------------------------------------------------

# 🚀 Passo 1 -- Instalar NGINX Ingress Controller (Baremetal)

## Criar diretório

``` bash
sudo mkdir -p /root/aplicacoes/ingress
```

## Baixar manifesto oficial

``` bash
curl -L https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/baremetal/deploy.yaml -o /root/aplicacoes/ingress/nginx-ingress-controller.yaml
```

## Ajustar externalIPs (LAB)

Edite o Service ingress-nginx-controller:

``` yaml
spec:
  type: NodePort
  externalIPs:
  - 192.168.0.32
```

⚠ Ambiente de laboratório.\
Em cloud normalmente usamos `Service type LoadBalancer`.

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

# 🌐 Configurar DNS Local

Adicionar no arquivo hosts:

    192.168.0.32   my-kubernetes.com.br

------------------------------------------------------------------------

# 🏗 Passo 2 -- Criar Aplicações

Aplicar seu arquivo ecommerce.yaml:

``` bash
kubectl apply -f ecommerce.yaml
```

Validar:

``` bash
kubectl get pods -n ecommerce
kubectl get svc -n ecommerce
```

------------------------------------------------------------------------

# 🔥 Passo 3 -- Criar Ingress Simples

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

Aplicar:

``` bash
kubectl apply -f ingress-pay.yaml
```

Verificar:

``` bash
kubectl get ingress -n ecommerce -w
```

Testar no navegador:

http://my-kubernetes.com.br

------------------------------------------------------------------------

# 🔍 Troubleshooting Essencial (Mentalidade SRE)

## ADDRESS não aparece

``` bash
kubectl get svc -n ingress-nginx
```

Verifique se o Service tem externalIP.

------------------------------------------------------------------------

## 404 Not Found

Verifique:

``` bash
kubectl describe ingress -n ecommerce
kubectl get svc -n ecommerce
```

Possíveis causas:

-   Namespace errado
-   Service não existe
-   Selector incorreto

------------------------------------------------------------------------

## 503 Service Unavailable

``` bash
kubectl get endpoints -n ecommerce
```

Se não houver endpoints, o Pod não está sendo selecionado.

------------------------------------------------------------------------

# 📈 O que você aprendeu

-   Fluxo HTTP dentro do Kubernetes
-   Diferença entre Ingress e Controller
-   Exposição externa em ambiente baremetal
-   Diagnóstico básico de erros

------------------------------------------------------------------------

# 🚀 Próximo Nível

Para fechar Ingress em nível SRE Jr:

-   Path-based routing
-   Host-based routing
-   TLS básico
-   Logs do controller

Ingress deixa de ser configuração e vira operação.
