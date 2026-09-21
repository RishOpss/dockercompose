# 10-Minute Video Script

## 0:00–0:45 — Introduction

Hello everyone.

In this project, I am demonstrating a multi-container application using Docker Compose.

The application is a Todo application with three services: a frontend, a Flask backend, and a PostgreSQL database.

The architecture is:

Browser -> Frontend -> Backend -> PostgreSQL.

## 0:45–1:30 — Project Structure

The project has three directories: frontend, backend, and database.

The root contains `docker-compose.yml`.

The frontend contains the HTML application and Nginx configuration.

The backend contains the Flask API.

The database directory contains the SQL initialization script.

## 1:30–3:30 — Compose File

The Compose file defines all three services.

The frontend is built from `./frontend` and maps port 8080 on the host to port 80 in the Nginx container.

The backend is built from `./backend` and runs on port 5000.

The database uses the PostgreSQL image.

The backend uses `DB_HOST=db`.

This is important because Docker Compose provides service discovery. The backend can find PostgreSQL using the service name `db`.

The database also has a health check, and the backend waits for the database to become healthy.

## 3:30–4:30 — Networking

All three containers are attached to `todo-network`.

The frontend communicates with the backend through HTTP.

The backend communicates with PostgreSQL through port 5432.

Inside the backend container, `localhost` would mean the backend container itself, not PostgreSQL.

Therefore the backend uses:

`db:5432`

## 4:30–5:30 — Backend

The Flask backend provides REST APIs for creating, reading, updating, and deleting Todo items.

When the user creates a Todo, the frontend sends an HTTP request to the backend.

The backend inserts the record into PostgreSQL.

## 5:30–6:15 — Frontend

Nginx serves the frontend.

The browser calls `/api/todos`.

Nginx proxies those API requests to the backend service.

This gives us a simple three-tier application architecture.

## 6:15–7:00 — Start Everything

Now I will start the complete application using:

`docker compose up --build`

Docker Compose builds the application images, pulls the PostgreSQL image, creates the network and volume, and starts the services.

This is the key benefit: the complete stack can be defined as code and started with one command.

## 7:00–8:00 — Application Demo

I will open:

`http://localhost:8080`

Now I can add a Todo such as "Learn Docker Compose".

The request travels from the browser to the frontend and backend, and the backend stores the data in PostgreSQL.

I can also mark the Todo as completed and delete it.

## 8:00–8:45 — Containers

I will run:

`docker compose ps`

We can see the frontend, backend, and database containers.

I can inspect individual services using:

`docker compose logs backend`

and:

`docker compose logs db`

## 8:45–9:30 — Persistence

PostgreSQL uses the named volume `postgres-data`.

The volume is mounted at `/var/lib/postgresql/data`.

Therefore the database data survives normal container recreation.

If I run `docker compose down -v`, the volume is also removed and the database data is deleted.

## 9:30–10:00 — Conclusion

We have successfully demonstrated a multi-container application using Docker Compose.

We created a frontend, backend, and PostgreSQL database.

We demonstrated container networking, service discovery, service dependencies, database persistence, and one-command startup.

The final architecture is:

Browser -> Frontend -> Backend -> PostgreSQL.

Thank you.
