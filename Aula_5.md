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

# 🧪 Exercícios – Aula 5: Namespaces

---

## 🎯 Objetivo dos exercícios

Fixar os conceitos de **Namespaces**, prática com `kubectl`, contexto atual e entendimento de recursos **namespaced x globais**.

👉 **Regra de ouro:** execute tudo manualmente, sem copiar tudo de uma vez.

---

## 🔹 Exercício 1 – Explorando Namespaces

1. Liste todos os namespaces do cluster.
2. Identifique quais namespaces já vêm criados por padrão.
3. Descreva o namespace `default`.
4. Exporte o YAML do namespace `default`.

📌 **Pergunta para fixar:**

* O namespace `default` possui Pods por padrão?

---

## 🔹 Exercício 2 – Criando e usando um Namespace

1. Crie um namespace chamado `treino`.
2. Liste os namespaces e confirme a criação.
3. Crie um Pod nginx **dentro do namespace `treino`**.
4. Liste os Pods **sem informar namespace**.
5. Liste os Pods informando explicitamente o namespace `treino`.

📌 **Pergunta para fixar:**

* Por que o Pod não aparece quando você roda `kubectl get pods` sem `-n`?

---

## 🔹 Exercício 3 – Analisando o Pod no Namespace

1. Exporte o Pod nginx do namespace `treino` em formato YAML.
2. Localize o campo `namespace` no manifesto.

📌 **Pergunta para fixar:**

* O namespace é definido no `spec` ou no `metadata`?

---

## 🔹 Exercício 4 – Alterando o namespace padrão do contexto

1. Verifique qual é o namespace padrão do contexto atual.
2. Configure o contexto atual para usar o namespace `treino`.
3. Liste os Pods sem informar namespace.
4. Confirme que o Pod nginx aparece.

📌 **Pergunta para fixar:**

* Por que essa técnica é útil em debug e troubleshooting?

---

## 🔹 Exercício 5 – Voltando ao namespace default

1. Altere o contexto atual para usar novamente o namespace `default`.
2. Liste os Pods.

📌 **Pergunta para fixar:**

* O Pod do namespace `treino` aparece?

---

## 🔹 Exercício 6 – Limpeza controlada

1. Delete o Pod nginx criado no namespace `treino`.
2. Delete o namespace `treino`.
3. Liste os namespaces para confirmar a remoção.

⚠️ **Atenção:**

> Lembre-se que apagar um namespace remove TODOS os recursos dentro dele.

---

## 🔹 Exercício 7 – Recursos namespaced vs globais

1. Liste todos os recursos **namespaced** do cluster.
2. Liste todos os recursos **não namespaced**.
3. Identifique pelo menos:

   * 3 recursos namespaced
   * 3 recursos globais

📌 **Pergunta para fixar:**

* Por que `Node` não pertence a um namespace?

---

## 🧠 Desafio extra (nível entrevista)

1. Crie dois namespaces: `dev` e `prod`.
2. Crie um Pod nginx em cada namespace.
3. Mostre que Pods com o mesmo nome podem existir em namespaces diferentes.

📌 **Pergunta final:**

* Como namespaces ajudam na organização de ambientes?

---

## ✅ Resultado esperado

Ao final dos exercícios você deve:

* Entender claramente como namespaces funcionam
* Saber alternar contexto sem erro
* Evitar apagar recursos errados
* Estar confortável usando namespaces no dia a dia

🔥 Se conseguiu fazer tudo sem consultar a aula, você dominou o tema.
