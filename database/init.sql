CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO todos (title, completed)
SELECT 'Learn Docker Compose', FALSE
WHERE NOT EXISTS (
    SELECT 1 FROM todos WHERE title = 'Learn Docker Compose'
);
