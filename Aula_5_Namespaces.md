# 📘 Aula 5 – Namespaces (Essencial)

## 🎯 Objetivo da Aula
- Entender o que são `Namespaces`
- Usar namespaces na prática
- Alternar o namespace padrão do contexto
- Saber a diferença entre recursos *namespaced* e *globais*

---

## 🔧 Conceito Essencial

`Namespaces` servem para **organizar e isolar recursos** dentro de um cluster Kubernetes.  
São muito usados para separar **ambientes**, **times** ou **aplicações**.

---

## 1️⃣ Listando Namespaces

    kubectl get namespace
    kubectl get ns

---

## 2️⃣ Explorando o Namespace `default`

    kubectl get ns default
    kubectl describe ns default

📌 O namespace `default` é o padrão quando nenhum outro é informado.

---

## 3️⃣ Criando um Namespace

Criando um namespace chamado `dev`:

    kubectl create ns dev

---

## 4️⃣ Criando um Pod em Outro Namespace

Criando um Pod nginx no namespace `dev`:

    kubectl run nginx --image=nginx -n dev

Listando pods sem informar namespace:

    kubectl get pods

➡️ Nenhum Pod aparece porque o contexto atual usa o namespace `default`.

---

## 5️⃣ Acessando Recursos em Outro Namespace

    kubectl get pod nginx -n dev
    kubectl get pod nginx -n dev -o yaml

📌 Observe o campo `metadata.namespace`.

---

## 6️⃣ Alterando o Namespace Padrão do Contexto

Configurar o contexto atual para usar `dev` como padrão:

    kubectl config set-context --current --namespace=dev

Verificar configuração:

    kubectl config view | grep namespace

Agora o Pod aparece sem usar `-n`:

    kubectl get pods

---

## 7️⃣ Voltando para o Namespace `default`

    kubectl config set-context --current --namespace=default

---

## 8️⃣ Limpeza

    kubectl delete pod nginx -n dev
    kubectl delete ns dev

⚠️ Deletar um namespace remove **todos os recursos dentro dele**.

---

## 9️⃣ Recursos Namespaced vs Globais

Listar recursos que pertencem a namespaces:

    kubectl api-resources --namespaced=true

Listar recursos globais:

    kubectl api-resources --namespaced=false

📌 Exemplos:
- **Namespaced**: Pod, Service, Deployment
- **Globais**: Node, Namespace, PersistentVolume

---

## 🧪 Exercício de Fixação

1. Crie um namespace chamado `treino`
2. Crie um Pod nginx dentro dele
3. Liste os Pods sem informar namespace
4. Liste os Pods usando `-n treino`
5. Configure o contexto para usar `treino`
6. Liste os Pods novamente
7. Volte o contexto para `default`
8. Delete o namespace `treino`

🔥 Se você entendeu por que o Pod “some” e “aparece”, você entendeu `Namespaces`.
