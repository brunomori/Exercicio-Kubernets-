# Aula1  – Criando a aplicação **Olá Mundo Container**

Esta versão segue **exatamente o conceito da aula**, mas adaptada para:

* Ubuntu
* usuário comum (sem `/root`)
* repetição fácil para fixar

Você pode executar **linha por linha** sem erro de permissão.

---

## 🎯 Objetivo

Criar uma aplicação **Olá Mundo** usando **Nginx em container**, construir a imagem e publicar na porta 8080.

---

## 1️⃣ Criar a estrutura de pastas da aplicação


📌 Adaptado para sua realidade:

```bash
mkdir -p ~/app_container/olamundo/html
```

Conferir:

```bash
pwd
ls -R
```

---

## 2️⃣ Criar o arquivo `index.html`

📌 Comando adaptado:

```bash
 touch index.html
```

```bash
 html/index.html 
<html>
 <head>
  <title>
   Olá Mundo Container!!!
  </title>
 </head>
 <body style="background-color: blue;">
  <h1 style="color: white">Olá Mundo Container!!!</h1>
 </body>
</html>
```

Verificar se foi criado corretamente:

```bash
cat html/index.html
```

---

## 3️⃣ Criar o Dockerfile (definição da imagem)

📌 Comando adaptado:

```bash
touch Dockerfile
```
Utiliza VIM  para edicação e salvar a atualização do index.html, segue conteudo. 

```bash
FROM nginx
COPY index.html /usr/share/nginx/html/
```

Conferir:

```bash
cat Dockerfile
```

---

## 4️⃣ Construir a imagem do container (Docker)

```bash
docker build -t nome_da_image .

```

Listar imagens:

```bash
docker images
```


## 5️⃣ Executar o container (Docker)

```bash
docker run -d -p 8080:80 nome_da_image

```

Verificar se está rodando:

```bash
docker ps
```

---

## 6️⃣ Acessar a aplicação no navegador

No **mesmo computador**:

```
http://localhost:8080
```

Você deve ver:

> **Olá Mundo Container!!!**

---

## 7️⃣ Comandos básicos (fixação)

### Listar containers

```bash
docker ps
```

### Listar imagens

```bash
docker images
```

### Parar container

```bash
docker stop k8s4dev-ola-mundo-container
```

### Remover container

```bash
docker rm -f k8s4dev-ola-mundo-container
```

### Remover imagem

```bash
docker rmi k8s4dev/ola-mundo-container-image:1.0.0
```

---

## 🧠 Conceitos que você fixou

* Estrutura de aplicação em container
* `Dockerfile` como definição da imagem
* `COPY` levando arquivos para dentro da imagem
* Diferença entre **imagem** e **container**
* Publicação de porta (`8080:80`)

---

## 🔁 Exercício de repetição (ESSENCIAL)

1. Apague tudo:

```bash
rm -rf ~/app_container
```

2. Refaça **sem copiar**
3. Mude o HTML
4. Rebuild a imagem
5. Rode novamente


🔁 Sequência AJUSTADA (ideal para fixar)

Essa é a versão que eu recomendo você repetir até virar automático:

docker ps -a 
docker build -t nome_da_image .
docker ps
docker run -d -p 8080:80 nome_da_image
docker stop nome_da_image
docker rm -f nome_da_image


Se conseguir fazer sem consultar, **o conceito está sólido** ✅
