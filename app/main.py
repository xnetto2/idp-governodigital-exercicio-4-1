from typing import Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Exercicio 4.1 - TODO list")


class TodoEntrada(BaseModel):
    titulo: str = Field(..., min_length=1)
    concluida: bool = False


class Todo(TodoEntrada):
    id: int


todos: Dict[int, Todo] = {}
proximo_id = 1


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/todos", response_model=Todo)
def criar_todo(todo_entrada: TodoEntrada):
    global proximo_id

    todo = Todo(id=proximo_id, **todo_entrada.dict())
    todos[proximo_id] = todo
    proximo_id += 1

    return todo


@app.get("/todos/{id}", response_model=Todo)
def ler_todo(id: int):
    todo = todos.get(id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Tarefa nao encontrada")

    return todo


@app.put("/todos/{id}", response_model=Todo)
def atualizar_todo(id: int, todo_entrada: TodoEntrada):
    if id not in todos:
        raise HTTPException(status_code=404, detail="Tarefa nao encontrada")

    todo = Todo(id=id, **todo_entrada.dict())
    todos[id] = todo

    return todo
