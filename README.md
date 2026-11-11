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

## Infraestrutura Virtual com Vagrant, VirtualBox e Ansible (VM1 e VM2)

O repositório define duas máquinas virtuais provisionadas com Vagrant utilizando o provedor **VirtualBox** e configuradas com **Ansible**:

- **VM1 (Nó de Controle Ansible / Máquina de Testes):**
  - **Memória RAM:** 1024 MB
  - **Endereço IPv4 Privado (Classe C):** `192.168.56.10`
  - **Softwares instalados:** `ansible`, `curl` e `wget`
  - **Configuração montada:** A pasta `./ansible` do repositório é montada em `/home/vagrant/ansible` dentro da VM1 (com links simbólicos em `/etc/ansible/ansible.cfg` e `/etc/ansible/hosts` apontando para os arquivos montados), além da geração automática da chave SSH (`ed25519`) utilizada pelo Ansible para acessar a VM2.
- **VM2 (Nó Gerenciado / Servidor Backend):**
  - **Memória RAM:** 1024 MB (dimensionada para execução estável do Ubuntu 22.04 LTS e do servidor FastAPI/Uvicorn).
  - **Endereço IPv4 Privado (Classe C):** `192.168.56.11`
  - **Provisionamento via Ansible:** Recebe a aplicação por meio do playbook `ansible/configuranode.yaml`, que clona o repositório em `/home/vagrant/hortas`, cria o ambiente virtual Python em `/home/vagrant/venv`, instala as dependências de `requirements.txt` e registra o serviço `hortas` no `systemd`.

### Arquivos do Ansible

Os arquivos de configuração e automação ficam armazenados no diretório `ansible/`:

- [`ansible/ansible.cfg`](ansible/ansible.cfg): arquivo de configuração do Ansible (inventário padrão `/home/vagrant/ansible/hosts`, usuário remoto `vagrant`, chave privada `/home/vagrant/.ssh/id_ed25519` e `host_key_checking = False`).
- [`ansible/hosts`](ansible/hosts): inventário contendo o grupo `[app]` com o host `vm2` (`192.168.56.11`).
- [`ansible/configuranode.yaml`](ansible/configuranode.yaml): playbook responsável por instalar `git`, `python3`, `python3-pip` e `python3-venv` na VM2, clonar o repositório da aplicação, instalar as dependências de execução e habilitar/iniciar o serviço `hortas`.

### Configuração e execução da infraestrutura e da aplicação

1. **Subir as máquinas virtuais:**
   No diretório raiz do projeto (onde está localizado o `Vagrantfile`), execute:

   ```bash
   vagrant up
   ```

   > Esse comando cria e inicia `vm1` e `vm2` no VirtualBox, instala o Ansible, `curl` e `wget` na `vm1`, monta `./ansible` em `/home/vagrant/ansible` e configura a chave SSH entre `vm1` e `vm2`.

2. **Verificar o estado das VMs:**
   ```bash
   vagrant status
   ```
   Ambas as máquinas (`vm1` e `vm2`) devem constar com o status `running (virtualbox)`.

3. **Acessar o nó de controle (`vm1`) e testar a conectividade com o Ansible:**
   ```bash
   vagrant ssh vm1
   ansible all -m ping
   ```
   A resposta esperada para `vm2` deve indicar `SUCCESS` com `"ping": "pong"`.

4. **Executar o playbook para instalar e iniciar a aplicação na `vm2`:**
   Ainda dentro da `vm1`, execute:

   ```bash
   ansible-playbook /home/vagrant/ansible/configuranode.yaml
   ```

   O playbook realiza o clone do repositório na `vm2` (`/home/vagrant/hortas`), cria o ambiente virtual em `/home/vagrant/venv`, instala todas as dependências do `requirements.txt`, configura o serviço `/etc/systemd/system/hortas.service` e inicia a API automaticamente ouvindo em `0.0.0.0:8080`.

5. **Gerenciar ou executar a aplicação manualmente na `vm2` (opcional):**
   Caso queira verificar o status do serviço ou executar o servidor manualmente na `vm2`:
   - Pelo `systemd` (dentro da `vm2`, via `vagrant ssh vm2`):
     ```bash
     sudo systemctl status hortas
     sudo systemctl restart hortas
     ```
   - Execução manual com Uvicorn (caso o serviço esteja parado via `sudo systemctl stop hortas`):
     ```bash
     cd /home/vagrant/hortas
     /home/vagrant/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080
     ```

### Testando a aplicação dentro da VM1 com `curl` ou `wget`

Com a infraestrutura provisionada e a API em execução na `vm2` (`192.168.56.11:8080`), execute os testes diretamente a partir da `vm1` (`192.168.56.10`):

1. **Acessar a VM1 via SSH (caso ainda não esteja conectado):**
   ```bash
   vagrant ssh vm1
   ```

2. **Testar a rota GET `/api/hortas` da aplicação na VM2:**
   - **Utilizando `curl`:**
     ```bash
     curl http://192.168.56.11:8080/api/hortas
     ```
     _(Opcional: para visualizar o código de status e os cabeçalhos HTTP, use `curl -i http://192.168.56.11:8080/api/hortas`)_

   - **Utilizando `wget`:**
     ```bash
     wget -qO- http://192.168.56.11:8080/api/hortas
     ```
     _(O parâmetro `-qO-` faz o `wget` exibir o corpo da resposta diretamente no terminal sem gerar arquivo local)_

   - **Testando a consulta de uma horta específica (ex.: ID `1`):**
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
