Claro\! Aqui está uma proposta de `README.md` que descreve seu projeto de forma profissional e atrativa, destacando os pontos que você mencionou.

Você pode copiar e colar este conteúdo diretamente em um arquivo `README.md` na raiz do seu projeto no GitHub.

-----

# 📚 API de Sistema de Biblioteca

Bem-vindo à API do Sistema de Biblioteca\! Este é um serviço de backend robusto e moderno, construído para gerenciar as operações de uma biblioteca digital, permitindo a consulta de livros e a gestão de reservas de forma eficiente e segura.

## 📖 Visão Geral

O projeto consiste em uma API RESTful que serve como o cérebro de um sistema de biblioteca. Através dela, os usuários podem interagir com o catálogo de livros, verificar a disponibilidade e realizar reservas. A segurança é um pilar central, com todas as rotas protegidas por um sistema de autenticação moderno baseado em JSON Web Tokens (JWT).

## ✨ Funcionalidades Principais

  - **Autenticação Segura de Usuários**: Sistema completo de registro e login com senhas criptografadas.
  - **Gerenciamento de JWT**: Geração de tokens de acesso na autenticação, com tempo de expiração para maior segurança.
  - **Consulta de Livros**: Endpoints para listar todos os livros ou buscar um livro específico pelo seu ID.
  - **Sistema de Reservas**: Funcionalidade para que usuários autenticados possam reservar um livro, diminuindo o número de cópias disponíveis.
  - **Cancelamento de Reservas**: Permite que o usuário cancele uma reserva existente, repondo a cópia no acervo.
  - **Middleware de Proteção**: Todas as rotas que exigem autenticação são protegidas, validando o token JWT a cada requisição.

## 🚀 Tecnologias Utilizadas (Stack)

Este projeto foi construído utilizando um conjunto de tecnologias modernas, focadas em performance, segurança e escalabilidade.

  - **Linguagem**: **Python 3.12+**
  - **Framework**: **FastAPI** - Um framework de alta performance, fácil de usar e que inclui validação de dados e documentação automática (Swagger UI / ReDoc).
  - **Banco de Dados**: **MongoDB** - Um banco de dados NoSQL flexível e escalável, ideal para armazenar documentos como livros e usuários de forma intuitiva.
  - **Autenticação**: **JWT (JSON Web Tokens)** - Utilizamos a biblioteca `python-jose` para implementar um fluxo de autenticação state-of-the-art, garantindo que apenas usuários autorizados acessem os recursos protegidos.
  - **Validação de Dados**: **Pydantic** - Integrado nativamente ao FastAPI, garante que todos os dados que entram e saem da API sejam válidos e sigam o esquema definido.
  - **Servidor ASGI**: **Uvicorn** - O servidor ASGI ultrarrápido que serve nossa aplicação.

## 🛡️ Destaque: Segurança com JWT

A autenticação da API é um dos seus pontos mais fortes. O fluxo funciona da seguinte maneira:

1.  O usuário envia suas credenciais para o endpoint `/login`.
2.  O servidor valida as informações e, se corretas, gera um **token JWT** assinado com uma chave secreta.
3.  Este token é retornado ao cliente, que deve armazená-lo de forma segura.
4.  Para acessar qualquer rota protegida (como `/books/{id}/reserve`), o cliente deve enviar o token no cabeçalho da requisição: `Authorization: Bearer <seu_token_aqui>`.
5.  Um middleware inteligente intercepta a requisição, valida a assinatura e a data de expiração do token antes de permitir o acesso à lógica da rota.

Este método garante que a API seja *stateless* e segura, protegendo os dados dos usuários e a integridade do sistema.



-----

## 🏁 Como Executar o Projeto (com Makefile)

Este projeto utiliza um `Makefile` para automatizar as tarefas mais comuns, como instalar dependências e iniciar o servidor. Certifique-se de ter o `make` instalado no seu sistema (geralmente já vem com Linux e macOS).

1.  **Clone o repositório:**

    ```bash
    git clone <url-do-seu-repositorio>
    cd <nome-do-projeto>
    ```

2.  **Configure as Variáveis de Ambiente:**

      - Antes de tudo, crie um arquivo `.env` na raiz do projeto. Você pode copiar o exemplo `.env.example` (se houver) para começar.
      - Adicione suas variáveis, como a `SECRET_KEY` para o JWT e a `DATABASE_URI` para a conexão com o MongoDB. Este passo é crucial.

3.  **Instale as Dependências:**

      - Este comando irá criar o ambiente virtual (`venv`) automaticamente e instalar todas as bibliotecas listadas no `requirements.txt`.

    <!-- end list -->

    ```bash
    make update
    ```

4.  **Execute a Aplicação:**

      - Para iniciar o servidor em **modo de desenvolvimento** (com hot-reload ativado):

    <!-- end list -->

    ```bash
    make dev
    ```

      - Para iniciar o servidor em **modo de produção** (otimizado para performance):

    <!-- end list -->

    ```bash
    make prod
    ```

    Após executar `make dev` ou `make prod`, a API estará disponível em `http://127.0.0.1:8000`.

5.  **Acesse a documentação interativa** em `http://127.0.0.1:8000/docs` para ver e testar todos os endpoints.

### 📦 Gerenciando Dependências

  - **Para adicionar uma nova biblioteca:**

      - Use o comando `make add`, especificando o pacote com a variável `PKG`. O `Makefile` irá instalar o pacote e atualizar seu `requirements.txt` automaticamente.

    <!-- end list -->

    ```bash
    make add PKG=requests
    make add PKG="pydantic-settings"
    ```

  - **Para atualizar as bibliotecas existentes:**

      - Se você alterou o `requirements.txt` manualmente ou baixou uma nova versão do projeto, basta rodar o comando de atualização novamente.

    <!-- end list -->

    ```bash
    make update
    ```