# Sistema de Gestão de Hortas Comunitárias

API REST em Python e FastAPI para consultar, cadastrar, atualizar e deletar hortas comunitárias. Os dados são
armazenados em memória e reiniciados sempre que a aplicação é encerrada.

## Requisitos

- Python 3.10 ou superior

## Instalação e execução

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

A aplicação fica disponível em `http://localhost:8080` e a documentação
interativa do FastAPI em `http://localhost:8080/docs`.

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
