# Multi-Container Todo Application Using Docker Compose

A three-tier Todo application demonstrating Docker Compose, container networking, service dependencies, and PostgreSQL persistence.

## Architecture - Rishabh

Browser -> Frontend (Nginx) -> Backend (Flask) -> Database (PostgreSQL)

## Services

### Frontend
- Nginx Alpine
- Serves HTML/CSS/JavaScript
- Host port: `8080`

### Backend
- Python Flask
- REST API
- Container port: `5000`
- Connects to PostgreSQL using `db:5432`

### Database
- PostgreSQL 16 Alpine
- Stores Todo records
- Persistent named volume: `postgres-data`

## Start

```bash
docker compose up --build
```

Or detached:

```bash
docker compose up --build -d
```

Open:

```text
http://localhost:8080
```

## Useful commands

```bash
docker compose ps
docker compose logs
docker compose logs backend
docker compose logs db
docker compose down
docker compose down -v
docker compose build --no-cache
```

## API

```text
GET    /api/health
GET    /api/todos
POST   /api/todos
PUT    /api/todos/<id>
DELETE /api/todos/<id>
```

## Networking

All services use the `todo-network` bridge network.

The backend connects to PostgreSQL with:

```text
DB_HOST=db
DB_PORT=5432
```

`db` is the Compose service name. Do not use `localhost` from the backend container to reach PostgreSQL.

## Persistence

PostgreSQL uses:

```yaml
postgres-data:/var/lib/postgresql/data
```

The data survives container recreation.

To intentionally delete the database volume:

```bash
docker compose down -v
```

## Assignment demonstration

1. Show the project structure.
2. Explain `docker-compose.yml`.
3. Explain the three services.
4. Run `docker compose up --build`.
5. Show `docker compose ps`.
6. Open `http://localhost:8080`.
7. Add, complete, and delete Todo items.
8. Show the backend and database logs.
9. Restart the containers and demonstrate persistence.
10. Explain the Docker network and named volume.

## Expected outcome

The complete application starts with one command:

```bash
docker compose up --build
```

and the services communicate successfully:

```text
Frontend -> Backend -> PostgreSQL
```
