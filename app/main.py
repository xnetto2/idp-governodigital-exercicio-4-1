from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field


app = FastAPI(title="Exercicio 4.1 - TODO list")


class TodoEntrada(BaseModel):
    titulo: str = Field(..., min_length=1)
    concluida: bool = False


class Todo(TodoEntrada):
    id: int


todos: Dict[int, Todo] = {}
proximo_id = 1


HTML = """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lista de tarefas</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f4f6f8;
      --panel: #ffffff;
      --text: #17202a;
      --muted: #64748b;
      --line: #d8dee6;
      --accent: #1769aa;
      --accent-dark: #0f4f86;
      --ok: #16803c;
      --danger: #b42318;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: Arial, Helvetica, sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    main {
      width: min(920px, calc(100% - 32px));
      margin: 0 auto;
      padding: 32px 0;
    }
    header {
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 20px;
    }
    h1 {
      margin: 0;
      font-size: 28px;
      line-height: 1.15;
    }
    .status {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      min-height: 36px;
      padding: 8px 12px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--panel);
      color: var(--muted);
      font-size: 14px;
      white-space: nowrap;
    }
    .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--danger);
    }
    .dot.ok { background: var(--ok); }
    section {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      margin-bottom: 16px;
    }
    form {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
    }
    input[type="text"] {
      width: 100%;
      min-height: 42px;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 0 12px;
      font-size: 16px;
    }
    button {
      min-height: 42px;
      border: 0;
      border-radius: 6px;
      padding: 0 14px;
      background: var(--accent);
      color: white;
      font-size: 15px;
      cursor: pointer;
    }
    button:hover { background: var(--accent-dark); }
    button.secondary {
      border: 1px solid var(--line);
      background: white;
      color: var(--text);
    }
    button.secondary:hover { background: #eef2f6; }
    .toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }
    .toolbar strong { font-size: 18px; }
    .list {
      display: grid;
      gap: 10px;
      min-height: 48px;
    }
    .task {
      display: grid;
      grid-template-columns: auto 1fr auto;
      align-items: center;
      gap: 12px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fbfcfd;
    }
    .task input { width: 18px; height: 18px; }
    .task-title {
      min-width: 0;
      word-break: break-word;
    }
    .task.done .task-title {
      color: var(--muted);
      text-decoration: line-through;
    }
    .badge {
      color: var(--muted);
      font-size: 13px;
      white-space: nowrap;
    }
    .empty {
      color: var(--muted);
      padding: 14px 0;
    }
    .message {
      min-height: 22px;
      color: var(--muted);
      font-size: 14px;
    }
    .message.error { color: var(--danger); }
    @media (max-width: 620px) {
      main { width: min(100% - 20px, 920px); padding-top: 20px; }
      header { align-items: flex-start; flex-direction: column; }
      form { grid-template-columns: 1fr; }
      button { width: 100%; }
      .toolbar { align-items: stretch; flex-direction: column; }
      .task { grid-template-columns: auto 1fr; }
      .badge { grid-column: 2; }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>Lista de tarefas</h1>
        <p class="message" id="message">API REST do exercício 4.1</p>
      </div>
      <div class="status"><span class="dot" id="health-dot"></span><span id="health-text">verificando API</span></div>
    </header>

    <section>
      <form id="task-form">
        <input id="title-input" type="text" placeholder="Nova tarefa" autocomplete="off" required>
        <button type="submit">Adicionar</button>
      </form>
    </section>

    <section>
      <div class="toolbar">
        <strong>Tarefas</strong>
        <button class="secondary" type="button" id="refresh-button">Atualizar</button>
      </div>
      <div class="list" id="task-list"></div>
    </section>
  </main>

  <script>
    const form = document.querySelector("#task-form");
    const input = document.querySelector("#title-input");
    const list = document.querySelector("#task-list");
    const message = document.querySelector("#message");
    const healthDot = document.querySelector("#health-dot");
    const healthText = document.querySelector("#health-text");
    const refreshButton = document.querySelector("#refresh-button");

    function setMessage(text, isError = false) {
      message.textContent = text;
      message.classList.toggle("error", isError);
    }

    async function request(path, options = {}) {
      const response = await fetch(path, {
        headers: { "Content-Type": "application/json" },
        ...options
      });
      if (!response.ok) {
        throw new Error("Erro HTTP " + response.status);
      }
      return response.json();
    }

    async function checkHealth() {
      try {
        await request("/health");
        healthDot.classList.add("ok");
        healthText.textContent = "API online";
      } catch (error) {
        healthDot.classList.remove("ok");
        healthText.textContent = "API indisponivel";
      }
    }

    function renderTasks(tasks) {
      list.innerHTML = "";
      if (!tasks.length) {
        const empty = document.createElement("div");
        empty.className = "empty";
        empty.textContent = "Nenhuma tarefa cadastrada.";
        list.appendChild(empty);
        return;
      }

      for (const task of tasks) {
        const row = document.createElement("div");
        row.className = "task" + (task.concluida ? " done" : "");

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = task.concluida;
        checkbox.addEventListener("change", async () => {
          try {
            await request("/tarefas/" + task.id, {
              method: "PUT",
              body: JSON.stringify({ titulo: task.titulo, concluida: checkbox.checked })
            });
            await loadTasks();
            setMessage("Tarefa atualizada.");
          } catch (error) {
            setMessage(error.message, true);
            checkbox.checked = task.concluida;
          }
        });

        const title = document.createElement("div");
        title.className = "task-title";
        title.textContent = task.titulo;

        const badge = document.createElement("div");
        badge.className = "badge";
        badge.textContent = "#" + task.id;

        row.append(checkbox, title, badge);
        list.appendChild(row);
      }
    }

    async function loadTasks() {
      const tasks = await request("/tarefas");
      renderTasks(tasks);
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const titulo = input.value.trim();
      if (!titulo) return;

      try {
        await request("/tarefas", {
          method: "POST",
          body: JSON.stringify({ titulo, concluida: false })
        });
        input.value = "";
        await loadTasks();
        setMessage("Tarefa adicionada.");
      } catch (error) {
        setMessage(error.message, true);
      }
    });

    refreshButton.addEventListener("click", async () => {
      try {
        await loadTasks();
        setMessage("Lista atualizada.");
      } catch (error) {
        setMessage(error.message, true);
      }
    });

    checkHealth();
    loadTasks().catch((error) => setMessage(error.message, true));
  </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def interface_web():
    return HTML


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tarefas", response_model=Todo)
def criar_todo(todo_entrada: TodoEntrada):
    global proximo_id

    todo = Todo(id=proximo_id, **todo_entrada.dict())
    todos[proximo_id] = todo
    proximo_id += 1

    return todo


@app.get("/tarefas", response_model=List[Todo])
def listar_todos():
    return list(todos.values())


@app.get("/tarefas/{id}", response_model=Todo)
def ler_todo(id: int):
    todo = todos.get(id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Tarefa nao encontrada")

    return todo


@app.put("/tarefas/{id}", response_model=Todo)
def atualizar_todo(id: int, todo_entrada: TodoEntrada):
    if id not in todos:
        raise HTTPException(status_code=404, detail="Tarefa nao encontrada")

    todo = Todo(id=id, **todo_entrada.dict())
    todos[id] = todo

    return todo
