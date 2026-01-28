# 📘 Aula 5 – Namespaces

---

## 🎯 Objetivo da aula

* Entender o que são **Namespaces** no Kubernetes
* Explorar o **Namespace default**
* Criar e utilizar **namespaces personalizados**
* Aprender a alternar o **namespace padrão do contexto atual**
* Entender quais recursos são **namespaced** e quais são **globais**

---

## 🔧 Conceito rápido

Namespaces servem para **organizar, isolar e segmentar recursos** dentro de um cluster Kubernetes.

Eles são muito usados para separar:

* ambientes (dev, hml, prod)
* times
* aplicações

---

## 1️⃣ Listando os Namespaces existentes

```bash
kubectl get namespace
kubectl get ns
```

📌 **Resultado esperado**

* Lista de namespaces como `default`, `kube-system`, `kube-public`, etc.

---

## 2️⃣ Explorando o Namespace default

### Obter informações básicas

```bash
kubectl get ns default
```

### Descrever o namespace

```bash
kubectl describe ns default
```

### Visualizar o manifesto YAML

```bash
kubectl get ns default -o yaml
```

📌 Observe atributos como:

* `metadata.name`
* `status.phase`

---

## 3️⃣ Criando um novo Namespace

Vamos criar um namespace chamado `dev`.

```bash
kubectl create ns dev
```

### Verificar criação

```bash
kubectl get ns
```

---

## 4️⃣ Criando um Pod no namespace dev

Criar um Pod nginx utilizando o namespace `dev`.

```bash
kubectl run nginx --image=nginx -n dev
```

---

## 5️⃣ Listando Pods (namespace default)

```bash
kubectl get pods
```

📌 **Resultado esperado**

* Nenhum Pod listado

➡️ Isso acontece porque o Pod foi criado no namespace `dev`, não no `default`.

---

## 6️⃣ Acessando recursos em outro Namespace

### Listar Pod no namespace dev

```bash
kubectl get pod nginx -n dev
```

### Visualizar YAML do Pod

```bash
kubectl get pod nginx -n dev -o yaml
```

📌 Observe o campo:

```yaml
namespace: dev
```

---

## 7️⃣ Configurando namespace padrão do contexto atual

Quando estamos debugando aplicações fora do `default`, é comum esquecer a flag `-n`.

Vamos configurar o contexto atual para usar `dev` como namespace padrão.

```bash
kubectl config set-context --current --namespace=dev
```

### Verificar configuração

```bash
kubectl config view | grep namespace
```

### Listar Pods novamente

```bash
kubectl get pods
```

📌 Agora o Pod nginx aparece sem precisar informar `-n dev`.

---

## 8️⃣ Revertendo para o namespace default

```bash
kubectl config set-context --current --namespace=default
```

---

## 9️⃣ Limpeza do ambiente

### Remover Pod do namespace dev

```bash
kubectl delete pod nginx -n dev
```

### Remover Namespace dev

```bash
kubectl delete ns dev
```

⚠️ **Atenção**

> Deletar um namespace remove **TODOS os recursos dentro dele**.
> Evite este comando em ambientes produtivos.

---

## 🔟 Recursos namespaced vs globais

### Listar recursos que fazem parte de um namespace

```bash
kubectl api-resources --namespaced=true
```

### Listar recursos globais (não namespaced)

```bash
kubectl api-resources --namespaced=false
```

📌 Exemplos:

* **Namespaced**: Pod, Service, Deployment, ConfigMap, Secret
* **Globais**: Node, Namespace, PersistentVolume

---

## 🧠 Conceitos fixados

* Namespace isola recursos logicamente
* O namespace padrão é `default`
* O contexto atual define o namespace padrão
* Nem todos os recursos pertencem a namespaces
* Deletar um namespace apaga tudo dentro dele

---

## 🔗 Referência oficial

* Kubernetes Namespaces
* [https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
