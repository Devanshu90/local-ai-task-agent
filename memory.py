import sqlite3
from pathlib import Path


DATABASE = Path("agent_memory.db")


def initialize_memory():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_key TEXT NOT NULL,
            memory_value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_memory(key, value):
    initialize_memory()

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO memories (memory_key, memory_value)
        VALUES (?, ?)
        """,
        (key, value)
    )

    connection.commit()
    connection.close()

    return f"Memory saved: {key} = {value}"


def recall_memory(query):
    initialize_memory()

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    search = f"%{query}%"

    cursor.execute(
        """
        SELECT memory_key, memory_value
        FROM memories
        WHERE memory_key LIKE ?
           OR memory_value LIKE ?
        ORDER BY id DESC
        LIMIT 10
        """,
        (search, search)
    )

    results = cursor.fetchall()

    connection.close()

    if not results:
        return "No matching memories found."

    output = []

    for key, value in results:
        output.append(f"{key}: {value}")

    return "\n".join(output)


def list_memories():
    initialize_memory()

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT memory_key, memory_value
        FROM memories
        ORDER BY id DESC
        """
    )

    results = cursor.fetchall()

    connection.close()

    if not results:
        return "No memories stored."

    output = []

    for key, value in results:
        output.append(f"{key}: {value}")

    return "\n".join(output)