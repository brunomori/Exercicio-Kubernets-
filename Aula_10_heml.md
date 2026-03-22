# 📦 Helm no Kubernetes — Guia Prático (SRE Jr)

Guia simples, direto e prático para seu primeiro contato com Helm.

---

# 🎯 Objetivo

Ao final deste guia você será capaz de:

- Entender o que é Helm
- Instalar e usar Helm no dia a dia
- Fazer deploy e upgrade de aplicações
- Entender rollback (essencial pra SRE)
- Fazer debug básico

---

# 🧠 O que é Helm?

Helm é o gerenciador de pacotes do Kubernetes.

📌 Ele resolve um problema real:
Gerenciar vários YAMLs manualmente é difícil.

👉 Com Helm você:
- Padroniza deploy
- Reutiliza configs
- Faz rollback fácil

---

# 📦 Conceitos principais

## Chart
Pacote com templates Kubernetes

## Release
Aplicação rodando no cluster

## values.yaml
Arquivo de configuração

---

# ⚙️ Instalação

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```

---

# 🔍 Repositório

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo nginx
```

---

# 🚀 Deploy (forma real usada em SRE)

```bash
helm upgrade --install meu-nginx bitnami/nginx
```

📌 Esse comando:
- Cria se não existir
- Atualiza se já existir

---

# 📁 Usando values.yaml

```bash
helm show values bitnami/nginx > values.yaml
```

Exemplo simples:

```yaml
service:
  type: NodePort
```

Aplicando:

```bash
helm upgrade --install meu-nginx bitnami/nginx -f values.yaml
```

---

# 🔍 Debug básico

Ver status:

```bash
helm status meu-nginx
```

Ver configurações:

```bash
helm get values meu-nginx
```

Simular deploy:

```bash
helm install meu-nginx bitnami/nginx --dry-run --debug
```

---

# 🔄 Rollback (ESSENCIAL)

Ver histórico:

```bash
helm history meu-nginx
```

Voltar versão:

```bash
helm rollback meu-nginx 1
```

---

# ⚠️ Namespace (uso real)

```bash
helm upgrade --install meu-nginx bitnami/nginx -n dev --create-namespace
```

---

# 💡 Dica SRE (simples e poderosa)

```bash
helm upgrade --install meu-nginx bitnami/nginx --atomic
```

📌 Se der erro → rollback automático

---

# 🧪 Exercício prático

1. Adicione o repositório bitnami  
2. Faça deploy de um nginx  
3. Crie um values.yaml e altere para NodePort  
4. Faça upgrade usando o values  
5. Veja o histórico  
6. Execute rollback  

---

# 🏁 Conclusão

Helm ajuda você a:

- Automatizar deploy
- Evitar erro manual
- Fazer rollback rápido
---
