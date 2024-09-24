# API de Gerenciamento de Usuários com JWT e Flask

Este projeto é uma API RESTful para gerenciar usuários, com autenticação baseada em tokens JWT. A API foi construída utilizando **Flask**, **Flask-RESTful**, **Flask-JWT-Extended**, e **Flask-OpenAPI**. A aplicação permite o registro, login, e gerenciamento de usuários, com segurança e autenticação via JWT.

#### Descrição Geral

O sistema foi desenvolvido para gerenciar contas de usuários, permitindo:

- Registro e login de novos usuários.
- Listagem de usuários cadastrados.
- Atualização e exclusão de contas de usuários.
- Verificação de credenciais de usuários.

#### Funcionalidades Principais

1. **Autenticação JWT**: Geração e verificação de tokens JWT para acessar rotas protegidas.
2. **Gerenciamento de Usuários**: Registro, login, listagem, atualização e exclusão de contas.
3. **Proteção de Rotas**: As rotas que manipulam dados sensíveis estão protegidas por JWT, garantindo a segurança do sistema.

---

## Requisitos

Crie um ambiente virtual para instalar as dependências do projeto:

Windows:
```
python -m venv venv
```
macOS e Linux:
```
python3 -m venv venv
```

Ative o ambiente virtual:

Windows:
```
venv\Scripts\activate
```
macOS e Linux:
```
source venv/bin/activate
```

Instale as dependências do projeto:

```
pip install -r requirements.txt
```

---

## Funcionalidades

### Configuração do CORS

O CORS (Cross-Origin Resource Sharing) foi habilitado para controlar quais origens podem fazer requisições à API, garantindo maior segurança.

#### 1. `CORS(app, resources={...})`

- Habilita o CORS no aplicativo Flask, controlando quais origens podem acessar a API.

#### 2. `r"/api/*"`

- A configuração se aplica a todas as rotas que começam com `/api/`.

#### 3. `"origins": "http://127.0.0.1:5000"`

- Somente a origem `http://127.0.0.1:5000` (geralmente o frontend local) está autorizada a acessar a API. Qualquer outra origem será bloqueada.

Essa configuração garante que apenas o frontend autorizado possa interagir com a API, prevenindo acessos não autorizados.

Trecho de código:

```python
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}})
```

---

## Endpoints

### 1. **Home**
- **Rota:** `/`
- **Método:** `GET`
- **Descrição:** Redireciona para a documentação Swagger da API.
- **Resposta:**
  - `302`: Redireciona para `/openapi/swagger`

---

### 2. **Listar Usuários**
- **Rota:** `/api/usuarios`
- **Método:** `GET`
- **Descrição:** Retorna uma lista de todos os usuários cadastrados. Esta rota está protegida por JWT.
- **Autenticação:** Token JWT obrigatório.
- **Segurança:** `Bearer Token`
- **Respostas:**
  - `200`: Lista de usuários retornada com sucesso.
  - `400`: Erro de requisição.
  - `401`: Acesso não autorizado.
  - `500`: Erro interno no servidor.

---

### 3. **Registrar Usuário**
- **Rota:** `/api/registrar`
- **Método:** `POST`
- **Descrição:** Registra um novo usuário no sistema.
- **Autenticação:** Não requer autenticação.
- **Corpo da Requisição:**
  - `nome` (string) - Nome do usuário.
  - `email` (string) - Email do usuário.
  - `senha` (string) - Senha do usuário.
- **Respostas:**
  - `201`: Usuário registrado com sucesso.
  - `400`: Erro de validação de dados.
  - `500`: Erro interno no servidor.

---

### 4. **Atualizar Usuário**
- **Rota:** `/api/usuario/<int:id>`
- **Método:** `PUT`
- **Descrição:** Atualiza as informações de um usuário existente.
- **Autenticação:** Token JWT obrigatório.
- **Segurança:** `Bearer Token`
- **Parâmetros da Rota:**
  - `id` (int) - ID do usuário.
- **Corpo da Requisição:**
  - `email` (string) - Novo email do usuário (opcional).
  - `senha` (string) - Nova senha do usuário (opcional).
- **Respostas:**
  - `200`: Usuário atualizado com sucesso.
  - `400`: Erro de validação de dados.
  - `404`: Usuário não encontrado.
  - `500`: Erro interno no servidor.

---

### 5. **Deletar Usuário**
- **Rota:** `/api/usuario/<int:id>`
- **Método:** `DELETE`
- **Descrição:** Remove um usuário do sistema pelo seu ID.
- **Autenticação:** Token JWT obrigatório.
- **Segurança:** `Bearer Token`
- **Parâmetros da Rota:**
  - `id` (int) - ID do usuário.
- **Respostas:**
  - `204`: Usuário removido com sucesso.
  - `404`: Usuário não encontrado.
  - `500`: Erro interno no servidor.

---

### 6. **Verificar Credenciais**
- **Rota:** `/api/verifica_senha`
- **Método:** `POST`
- **Descrição:** Verifica se o email e senha do usuário estão corretos.
- **Autenticação:** Não requer autenticação.
- **Corpo da Requisição:**
  - `email` (string) - Email do usuário.
  - `senha` (string) - Senha do usuário.
- **Respostas:**
  - `200`: Credenciais verificadas com sucesso.
  - `400`: Erro de validação de dados.
  - `401`: Credenciais inválidas.
  - `500`: Erro interno no servidor.

---

## Erros Comuns

- `400` - Erro de Requisição: Quando os dados fornecidos na requisição são inválidos.
- `401` - Não Autorizado: Quando o token JWT está ausente ou inválido.
- `404` - Não Encontrado: Quando o recurso solicitado não existe.
- `500` - Erro Interno do Servidor: Problemas ao processar a requisição no servidor.

---

## Executando o Projeto

Para iniciar o servidor de desenvolvimento, execute:

```
python app.py
```

O servidor será iniciado em `http://localhost:5001`.

---

# Docker

Exemplo genérico.

#### 1. **Instalação do Docker**

**Para Windows e Mac:**
- **Baixe e instale o Docker Desktop**:
  - Acesse o [site do Docker Desktop](https://www.docker.com/products/docker-desktop) e baixe o instalador apropriado para seu sistema operacional.
  - Siga as instruções do instalador. Durante a instalação, pode ser necessário habilitar o WSL 2 (para Windows).

**Para Linux:**
- **Instalação do Docker**:
  - Abra um terminal e execute os seguintes comandos para instalar o Docker:
    ```bash
    sudo apt-get update
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        software-properties-common

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt-get install -y docker-ce
    ```

- **Iniciar o serviço Docker**:
    ```bash
    sudo systemctl start docker
    sudo systemctl enable docker
    ```

- **Verificar se o Docker está rodando**:
    ```bash
    sudo docker run hello-world
    ```

#### 2. **Criar a Estrutura do Projeto**

Agora que o Docker está instalado, você precisa criar a estrutura de pastas para sua aplicação Flask. Execute os seguintes comandos no terminal:

```bash
mkdir minha-app-flask
cd minha-app-flask
touch app.py requirements.txt Dockerfile docker-compose.yml
```

### 3. **Escrever o Código da Aplicação**

Abra o arquivo `app.py` e adicione o seguinte código básico para a aplicação Flask:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Olá, Docker!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 4. **Criar o arquivo requirements.txt**

No arquivo `requirements.txt`, adicione a seguinte linha para instalar o Flask:

```
Flask==2.0.3
```

### 5. **Criar o Dockerfile**

No arquivo `Dockerfile`, cole o seguinte código:

```dockerfile
# Usa a imagem base do Python
FROM python:3.9.10-slim-buster

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho no container
COPY requirements.txt ./

# Instala as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do projeto para o diretório de trabalho
COPY . .

# Define o comando para rodar a aplicação
CMD ["python", "app.py"]
```

### 6. **Criar o docker-compose.yml**

No arquivo `docker-compose.yml`, cole o seguinte código:

```yaml
version: '3.5'

services:
  flask-app-service:
    build: .  # Aponta para o diretório atual
    ports:
      - "5000:5000"  # Mapeia a porta 5000 do container para a porta 5000 do host
    environment:
      - PYTHONUNBUFFERED=1  # Para garantir que os logs sejam exibidos em tempo real
```

### 7. **Rodar a Aplicação**

Com todos os arquivos configurados, agora você pode rodar a aplicação Flask com Docker. No terminal, na pasta `minha-app-flask`, execute o seguinte comando:

```bash
docker-compose up --build
```

Esse comando irá:
- Construir a imagem Docker da sua aplicação.
- Iniciar um container executando sua aplicação Flask.

### 8. **Acessar a Aplicação**

Depois que o comando acima for executado, abra o seu navegador e vá para `http://localhost:5000`. Você deve ver a mensagem "Olá, Docker!".

# Estrutura

![alt text](image.png)