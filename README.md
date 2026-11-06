# Sistema de Gestão de Hortas Comunitárias

API REST em Python e FastAPI para consultar, cadastrar, atualizar e deletar hortas comunitárias. Os dados são
armazenados em memória e reiniciados sempre que a aplicação é encerrada.

[![Docker Image Size](https://img.shields.io/docker/image-size/vinisoaresti/vinisoaresti)](https://hub.docker.com/r/vinisoaresti/vinisoaresti)
[![Docker Pulls](https://img.shields.io/docker/pulls/vinisoaresti/vinisoaresti)](https://hub.docker.com/r/vinisoaresti/vinisoaresti)
[![Docker Image Version](https://img.shields.io/docker/v/vinisoaresti/vinisoaresti)](https://hub.docker.com/r/vinisoaresti/vinisoaresti)
[![Docker Stars](https://img.shields.io/docker/stars/vinisoaresti/vinisoaresti)](https://hub.docker.com/r/vinisoaresti/vinisoaresti)

## Requisitos

- Docker instalado (opcional, para execução via container)
- [VirtualBox](https://www.virtualbox.org/) e [Vagrant](https://www.vagrantup.com/) instalados (para execução da infraestrutura virtual)

## Criação da imagem e execução

Criação:

```shell
docker build -t hortas-api .
```

Execução:

```shell
docker run -d -p 8080:8080 --name hortas-app hortas-api
```

A aplicação fica disponível em `http://localhost:8080/api/hortas` e a documentação
interativa do FastAPI em `http://localhost:8080/docs`.

## Imagens no DockerHub

O repositório das imagens fica [aqui](https://hub.docker.com/r/vinisoaresti/vinisoaresti).

## Infraestrutura Virtual com Vagrant e VirtualBox (VM1 e VM2)

O repositório inclui a definição de duas máquinas virtuais provisionadas com Vagrant utilizando o provedor **VirtualBox**:

- **VM1 (Máquina de Testes / Cliente):**
  - **Memória RAM:** 1024 MB
  - **Endereço IPv4 Privado (Classe C):** `192.168.56.10`
  - **Ferramentas:** `curl` e `wget` pré-instaladas para execução de testes de rede e consumo de APIs.
- **VM2 (Servidor Backend):**
  - **Memória RAM:** 1024 MB (quantidade necessária e dimensionada para execução estável do sistema operacional Ubuntu 22.04 LTS e do servidor FastAPI/Uvicorn).
  - **Endereço IPv4 Privado (Classe C):** `192.168.56.11`
  - **Pasta Sincronizada:** A pasta raiz da aplicação é sincronizada com o diretório `/vagrant_data` dentro da VM2.
  - **Dependências:** `python3`, `python3-pip` e dependências do arquivo `requirements.txt` instaladas em ambiente virtual dedicado.
  - **Execução:** A aplicação FastAPI é iniciada automaticamente em segundo plano como um serviço de sistema (`systemd`), ouvindo em `0.0.0.0:8080`.

### Passo a passo para executar a infraestrutura

1. **Subir as máquinas virtuais:**
   No diretório raiz do projeto (onde está localizado o `Vagrantfile`), execute:

   ```bash
   vagrant up
   ```

   > Esse comando inicializará a VM1 e a VM2 no VirtualBox, montará o diretório sincronizado `/vagrant_data` na VM2, instalará todas as dependências do projeto e iniciará o backend automaticamente.

2. **Verificar o estado das VMs:**
   ```bash
   vagrant status
   ```
   Ambas as máquinas (`vm1` e `vm2`) devem constar com o status `running (virtualbox)`.

### Testando a rota GET dentro da VM1

Com as máquinas em execução e o backend ativo na VM2 (`192.168.56.11:8080`), realize os testes a partir da VM1 (`192.168.56.10`):

1. **Acessar a VM1 via SSH:**

   ```bash
   vagrant ssh vm1
   ```

2. **Testar a rota GET `/api/hortas` da aplicação na VM2:**
   - **Utilizando o `curl`:**

     ```bash
     curl http://192.168.56.11:8080/api/hortas
     ```

     _(Opcional: para visualizar com cabeçalhos de resposta HTTP, use `curl -i http://192.168.56.11:8080/api/hortas`)_

   - **Utilizando o `wget`:**

     ```bash
     wget -qO- http://192.168.56.11:8080/api/hortas
     ```

     _(O parâmetro `-qO-` faz o `wget` exibir o corpo da resposta diretamente no terminal de forma silenciosa)_

   - **Testando rota GET de uma horta específica (ex: ID 1):**
     - Com `curl`:
       ```bash
       curl http://192.168.56.11:8080/api/hortas/1
       ```
     - Com `wget`:
       ```bash
       wget -qO- http://192.168.56.11:8080/api/hortas/1
       ```

3. **Encerrar a sessão SSH na VM1:**
   ```bash
   exit
   ```

## Endpoints

### `GET /api/hortas`

Retorna a lista de hortas comunitárias:

```bash
curl http://localhost:8080/api/hortas
```

Exemplo de resposta:

```json
[
  {
    "id": 1,
    "nome": "Horta Comunitária Esperança",
    "localizacao": "Bairro Jardim das Flores",
    "responsavel": "Maria Silva",
    "area": 450.0
  }
]
```

### `POST /api/hortas`

Cadastra uma nova horta na mesma lista em memória consultada pelo endpoint
`POST /api/hortas`. O campo `id` é gerado automaticamente pela aplicação.

Exemplo de requisição:

```bash
curl -X POST http://localhost:8080/api/hortas \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Horta Sol Nascente",
    "localizacao": "Bairro Primavera",
    "responsavel": "Carlos Souza",
    "area": 180.5
  }'
```

JSON enviado na requisição:

```json
{
  "nome": "Horta Sol Nascente",
  "localizacao": "Bairro Primavera",
  "responsavel": "Carlos Souza",
  "area": 180.5
}
```

Em caso de sucesso, a API retorna o status HTTP `201 Created` e os dados da
horta cadastrada, incluindo o `id` gerado:

```json
{
  "id": 4,
  "nome": "Horta Sol Nascente",
  "localizacao": "Bairro Primavera",
  "responsavel": "Carlos Souza",
  "area": 180.5
}
```

### `GET /api/hortas/{id}`

Retorna os dados de uma horta comunitária específica existente na memória a partir do seu identificador (`id`).

Exemplo de requisição:

```bash
curl http://localhost:8080/api/hortas/1
```

Em caso de sucesso:

- **`200 OK`**: A API retorna os dados da horta encontrada:

```json
{
  "id": 1,
  "nome": "Horta Comunitária Esperança",
  "localizacao": "Bairro Jardim das Flores",
  "responsavel": "Maria Silva",
  "area": 450.0
}
```

Em casos de erro:

- **`404 Not Found` (Horta não encontrada)**: Retornado quando não existe horta cadastrada com o `id` informado.

Exemplo de resposta (`404`):

```json
{
  "detail": "Horta não encontrada"
}
```

### `PUT /api/hortas/{id}`

Atualiza os dados de uma horta comunitária existente na memória a partir do seu identificador (`id`).

Exemplo de requisição:

```bash
curl -X PUT http://localhost:8080/api/hortas/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Horta Comunitária Esperança Renovada",
    "localizacao": "Bairro Jardim das Flores",
    "responsavel": "Maria Silva",
    "area": 500.0
  }'
```

JSON enviado na requisição:

```json
{
  "nome": "Horta Comunitária Esperança Renovada",
  "localizacao": "Bairro Jardim das Flores",
  "responsavel": "Maria Silva",
  "area": 500.0
}
```

Em caso de sucesso:

- **`200 OK`**: A horta é atualizada com sucesso na memória e a API retorna os dados atualizados:

```json
{
  "id": 1,
  "nome": "Horta Comunitária Esperança Renovada",
  "localizacao": "Bairro Jardim das Flores",
  "responsavel": "Maria Silva",
  "area": 500.0
}
```

Em casos de erro:

- **`404 Not Found` (Horta não encontrada)**: Retornado quando não existe horta cadastrada com o `id` informado.

Exemplo de resposta (`404`):

```json
{
  "detail": "Horta não encontrada"
}
```

- **`422 Unprocessable Content` (Erro de Validação)**: Retornado quando o payload enviado possui campos obrigatórios ausentes ou tipos incompatíveis.

### `DELETE /api/hortas/{id}`

Remove uma horta comunitária cadastrada em memória a partir do seu identificador (`id`).

Exemplo de requisição:

```bash
curl -X DELETE http://localhost:8080/api/hortas/1
```

Em caso de sucesso:

- **`204 No Content`**: A horta é removida com sucesso da memória e a API não retorna conteúdo no corpo da resposta.

Em casos de erro:

- **`404 Not Found` (Horta não encontrada)**: Retornado quando não existe horta cadastrada com o `id` informado.

Exemplo de resposta (`404`):

```json
{
  "detail": "Horta não encontrada"
}
```

Também é possível iniciar diretamente com o Uvicorn:

```bash
uvicorn main:app --host 127.0.0.1 --port 8080
```

## Workflow de desenvolvimento

O workflow adotado neste projeto foi o **GitHub Flow**, por ser simples, leve e
adequado para um projeto universitário. A branch `main` representa a versão
estável do sistema. Cada nova funcionalidade é desenvolvida separadamente em
uma branch de feature e, depois de revisada, é integrada à `main` por meio de
um Pull Request.

Essa abordagem foi escolhida porque facilita a organização das alterações,
permite revisar o código antes da integração e reduz o risco de afetar a versão
estável durante o desenvolvimento.
