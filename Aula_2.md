# Aula 2 – Kubernetes Básico: Pods com Nginx

Esta aula dá continuidade ao **conceito de containers**, agora no **Kubernetes**, criando nosso **primeiro Pod** com Nginx.

Adaptado para:

* Ubuntu
* Kubernetes local (k3s, kind, minikube, etc.)
---

## 🎯 Objetivo da aula

* Verificar se o Kubernetes está rodando
* Criar um **Pod** usando `kubectl run`
* Inspecionar o Pod
* Entender por que ele **não é acessível externamente**
* Usar `port-forward` (debug)
* Criar o **manifesto YAML** do Pod

---

## 1️⃣ Verificar se o Kubernetes está rodando

Listar os nodes do cluster:

```bash
kubectl get nodes
```

✅ Resultado esperado:

* Pelo menos **1 node**
* Status: **Ready**

---

## 2️⃣ Verificar o namespace default

Checar se não há pods rodando:

```bash
kubectl get pods
```

✅ Resultado esperado:

```
No resources found in default namespace.
```

---

## 3️⃣ Criar o Pod Nginx (imperativo)

Criar o pod usando a imagem oficial do Docker Hub:

```bash
kubectl run nginx-run-pod --image=nginx
```

Verificar o status:

```bash
kubectl get pod nginx-run-pod
```

Quando o STATUS for **Running**, o pod está ativo.

---

## 4️⃣ Inspecionar o Pod

### Ver detalhes em YAML:

```bash
kubectl get pod nginx-run-pod -o yaml
```

### Obter o IP do Pod:

```bash
kubectl get pod nginx-run-pod -o yaml | grep IP
```

Exemplo:

```
podIP: 10.42.0.3
```

---

## 5️⃣ Acessar o Nginx pelo IP do Pod (teste interno)

```bash
curl 10.42.0.3
```

✅ Resultado esperado: Página padrão do **Welcome to nginx!**

📌 Isso funciona porque:

* O acesso acontece **dentro do cluster**

---

## 6️⃣ Tentar acessar pelo IP da máquina (falha esperada)

```bash
curl 192.168.0.32
```

❌ Resultado esperado:

```
curl: (7) Failed to connect to 192.168.0.32 port 80: Connection refused
```

📌 O Pod **não está exposto externamente**.

---

## 7️⃣ Expor o Pod com port-forward (DEBUG)

```bash
kubectl port-forward pod/nginx-run-pod :80 --address=0.0.0.0
```

Exemplo de saída:

```
Forwarding from 0.0.0.0:39495 -> 80
```

---

## 8️⃣ Acessar no navegador

Abra no browser:

```
http://IP_DA_SUA_MAQUINA:39495
```

Você verá:

> **Welcome to nginx!**

⚠️ IMPORTANTE:

* `port-forward` é **apenas para debug e desenvolvimento**
* Não é solução de produção

---

## 9️⃣ Deletar o Pod

```bash
kubectl delete pod nginx-run-pod
```

Verificar:

```bash
kubectl get pods
```

---

## 🔟 Manifesto YAML do Pod

Este é o manifesto equivalente ao `kubectl run`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: nginx-run-pod
  name: nginx-run-pod
spec:
  containers:
  - image: nginx
    name: nginx-run-pod
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
```

---

## 1️⃣1️⃣ Criar o arquivo YAML do Pod (adaptado)

Criar diretório para manifests:

```bash
mkdir -p ~/k8s/pods
```

Criar o arquivo:

```bash
cat > ~/k8s/pods/nginx-run-pod.yaml << EOF
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: nginx-run-pod
  name: nginx-run-pod
spec:
  containers:
  - image: nginx
    name: nginx-run-pod
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
EOF
```

Aplicar o manifesto:

```bash
kubectl apply -f ~/k8s/pods/nginx-run-pod.yaml
```

---

## 🧠 Conceitos fixados nesta aula

* Pod = **menor unidade do Kubernetes**
* Pod ≠ Container (pode ter mais de um)
* `kubectl run` cria **1 instância**
* Pod não é acessível externamente por padrão
* `port-forward` é solução **temporária**
* YAML é a forma declarativa (produção)

---

## 🔁 Exercício de fixação (obrigatório)

1. Delete o pod
2. Recrie com `kubectl run`
3. Delete novamente
4. Crie usando o YAML
5. Use `port-forward`

Se fizer sem olhar, o conceito está sólido ✅

---

## 🔜 Próxima aula

* Deployments (réplicas)
* Alta disponibilidade
* Exposição correta com **Service**
