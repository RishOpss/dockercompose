import os
import time
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "todo_db"),
    "user": os.getenv("DB_USER", "todo_user"),
    "password": os.getenv("DB_PASSWORD", "todo_password"),
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def initialize_database():
    for attempt in range(10):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Database connection successful.")
            return
        except Exception as exc:
            print(f"Database not ready: {exc}")
            time.sleep(2)
    raise RuntimeError("Could not connect to PostgreSQL.")

@app.get("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "backend"})

@app.get("/api/todos")
def get_todos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, completed FROM todos ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([
        {"id": row[0], "title": row[1], "completed": row[2]}
        for row in rows
    ])

@app.post("/api/todos")
def create_todo():
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO todos (title) VALUES (%s) RETURNING id, title, completed",
        (title,)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": row[0], "title": row[1], "completed": row[2]}), 201

@app.put("/api/todos/<int:todo_id>")
def update_todo(todo_id):
    data = request.get_json() or {}
    completed = bool(data.get("completed", False))

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE todos SET completed=%s WHERE id=%s RETURNING id,title,completed",
        (completed, todo_id)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if row is None:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify({"id": row[0], "title": row[1], "completed": row[2]})

@app.delete("/api/todos/<int:todo_id>")
def delete_todo(todo_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id=%s RETURNING id", (todo_id,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if row is None:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify({"message": "Todo deleted"})

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)
