# DB Final Project — FastAPI + PostgreSQL (Countries API)

REST API проект на **FastAPI**, работающий с **PostgreSQL** через **SQLAlchemy**.
В проекте реализован CRUD для сущности `Country` и пагинация списка.

---

## Stack (FastAPI / SQLAlchemy / Alembic и около того)

- **FastAPI** — REST API
- **SQLAlchemy** — ORM для работы с БД
- **Alembic** — инструмент для миграций (можно подключить/использовать для версионирования схемы)
- **PostgreSQL** — СУБД
- **psycopg2-binary** — драйвер PostgreSQL для Python
- **Uvicorn** — ASGI сервер для запуска FastAPI
- **Pydantic** — схемы и валидация данных (используется FastAPI)

---

## Project structure

DB_finalProject/
main.py
scripts/
init_db.sql
sql/
schema.sql


- `main.py` — приложение FastAPI + SQLAlchemy модель `Country`
- `scripts/init_db.sql` — создание базы `DB_finalProject` и установка владельца
- `scripts/sql/schema.sql` — вспомогательные SQL (схема/данные/черновики)

---

## Install dependencies

```bash
python3 -m pip install fastapi uvicorn sqlalchemy psycopg2-binary
python3 -m pip install alembic

PostgreSQL (macOS / Homebrew)

Проверка, что Postgres запущен:

brew services list | grep -i postgres
pg_isready -h localhost -p 5432

Запуск (если выключен):

brew services start postgresql@16

DB initialization

Создание базы данных DB_finalProject:

Запуск из корня репозитория
cd ~/DB_finalProject
psql -d postgres -f scripts/init_db.sql

Проверка, что база существует:

psql -d postgres -c "\l" | grep DB_finalProject

Если база уже создана, PostgreSQL

psql -d postgres -c "DROP DATABASE IF EXISTS \"DB_finalProject\";"

Run application
cd ~/DB_finalProject
python3 -m uvicorn main:app --reload


Swagger UI:

http://127.0.0.1:8000/docs

DB connection

В main.py используется строка подключения:

DATABASE_URL = "postgresql://arutunyandavid@127.0.0.1:5432/DB_finalProject"

API
Country fields

id (int)

name (str)

capital (str)

government_type (str)

Endpoints

GET / — healthcheck

POST /countries — create

GET /countries — list (pagination)

GET /countries/{country_id} — get by id

PUT /countries/{country_id} — update

DELETE /countries/{country_id} — delete

Pagination

GET /countries поддерживает:

limit (default 50, max 200)

offset (default 0)

Пример:

curl "http://127.0.0.1:8000/countries?limit=2&offset=0"
curl "http://127.0.0.1:8000/countries?limit=2&offset=2"

curl examples
Create
curl -X POST "http://127.0.0.1:8000/countries" \
  -H "Content-Type: application/json" \
  -d '{"name":"Japan","capital":"Tokyo","government_type":"Constitutional monarchy"}'

List
curl "http://127.0.0.1:8000/countries?limit=50&offset=0"

Get by id
curl "http://127.0.0.1:8000/countries/1"

Update
curl -X PUT "http://127.0.0.1:8000/countries/1" \
  -H "Content-Type: application/json" \
  -d '{"name":"Japan Updated","capital":"Tokyo","government_type":"Constitutional monarchy"}'

Delete
curl -X DELETE "http://127.0.0.1:8000/countries/1"

PostgreSQL check
psql -d DB_finalProject -c "\dt"
psql -d DB_finalProject -c "SELECT COUNT(*) FROM countries;"