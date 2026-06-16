# Exercício 4.1 - API REST TODO list

Este repositório contém uma API REST simples de lista de tarefas, implementada com FastAPI para o exercício 4.1.

A aplicação mantém as tarefas apenas em memória, sem banco de dados e sem persistência em arquivo. Os ids são incrementais e começam em 1. Cada tarefa é representada em JSON no formato:

```json
{
  "id": 1,
  "titulo": "Estudar Governo Digital",
  "concluida": false
}
```

## Endpoints

- `GET /health`: retorna `{"status":"ok"}`
- `POST /tarefas`: cria uma nova tarefa
- `GET /tarefas/{id}`: consulta uma tarefa pelo id
- `PUT /tarefas/{id}`: atualiza uma tarefa existente

A API retorna erro 404 quando o id informado não existe.

## Como rodar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o servidor local:

```bash
uvicorn app.main:app --port 8000
```

Depois acesse a API em:

```text
http://localhost:8000
```

Ao abrir esse endereço no navegador, a aplicação mostra uma interface web
simples para cadastrar, listar e marcar tarefas como concluídas.

## Exemplos de uso

Criar uma tarefa:

```bash
curl -X POST http://localhost:8000/tarefas \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Estudar API REST","concluida":false}'
```

Consultar uma tarefa:

```bash
curl http://localhost:8000/tarefas/1
```

Atualizar uma tarefa:

```bash
curl -X PUT http://localhost:8000/tarefas/1 \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Estudar API REST com FastAPI","concluida":true}'
```
