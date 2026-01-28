# Docker básico – Aplicação Olá Mundo com Nginx

Este guia é **curto, repetível e direto**, feito para você **executar várias vezes até fixar o conceito**.

Objetivo: criar uma **imagem Docker** que serve um HTML simples usando **Nginx**.

---

## 1️⃣ Criar a pasta do projeto

Escolha um local na sua home (exemplo: Área de Trabalho):

```bash
mkdir -p ~/Área\ de\ Trabalho/app_web
cd ~/Área\ de\ Trabalho/app_web
```

Conferir onde você está:

```bash
pwd
```

---

## 2️⃣ Criar o arquivo HTML

Crie o arquivo:

```bash
touch index.html
```

Edite:

```bash
nano index.html
```

Conteúdo de exemplo:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Olá Mundo</title>
</head>
<body>
  <h1>Olá Mundo 🚀</h1>
</body>
</html>
```

Salvar:

* `Ctrl + O` → Enter
* `Ctrl + X`

---

## 3️⃣ Criar a pasta `html`

O Nginx espera os arquivos dentro de `/usr/share/nginx/html`.

Vamos organizar:

```bash
mkdir html
mv index.html html/
```

Conferir estrutura:

```bash
ls -R
```

Resultado esperado:

```
app_web/
├── html/
│   └── index.html
```

---

## 4️⃣ Criar o Dockerfile

Ainda dentro da pasta do projeto:

```bash
cat > Dockerfile << EOF
FROM nginx
COPY html /usr/share/nginx/html
EOF
```

Conferir:

```bash
cat Dockerfile
```

---

## 5️⃣ Buildar a imagem Docker

```bash
docker build -t olamundo .
```

Ver imagens:

```bash
docker images
```

---

## 6️⃣ Rodar o container

```bash
docker run -p 8080:80 olamundo
```

Abra no navegador:

```bash
xdg-open http://localhost:8080
```

Você deve ver o **Olá Mundo**.

---

## 7️⃣ Parar o container

No terminal onde ele está rodando:

```bash
Ctrl + C
```

---

## 🧠 Conceitos fixados

* 📦 **Imagem**: template imutável (Dockerfile → docker build)
* ▶️ **Container**: imagem em execução (docker run)
* 🌐 **Porta**: `8080:80` (máquina → container)
* 📁 **COPY**: envia arquivos locais para dentro da imagem

---

## 🔁 Exercício de repetição (faça sempre)

1. Apague tudo:

```bash
rm -rf app_web
```

2. Refaça **do zero** sem olhar
3. Mude o texto do HTML
4. Rebuild a imagem
5. Rode de novo

Se conseguir repetir sem erro, o conceito **fixou** ✅

---

💡 Próximo passo sugerido:

* Usar `docker run -d`
* Nomear container (`--name`)
* Versionar com Git
