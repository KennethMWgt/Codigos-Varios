import sqlite3

DB_FILE = "todo.db"

def get_conn(db_file: str = DB_FILE) -> sqlite3.Connection:
    """Crea y retorna una conexión a la base SQLite."""
    conn = sqlite3.connect(db_file)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def create_tables(conn: sqlite3.Connection) -> None:
    """Crea la tabla de tareas si no existe."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            is_done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
    """)
    conn.commit()

def insert_task(conn: sqlite3.Connection, title: str) -> int:
    """Inserta una tarea nueva y retorna el id generado."""
    cur = conn.execute("INSERT INTO tasks (title) VALUES (?);", (title,))
    conn.commit()
    return cur.lastrowid

def update_task(conn: sqlite3.Connection, task_id: int, title: str = None, done: int = None) -> int:
    """Actualiza título y/o estado de una tarea. Retorna # de filas afectadas."""
    sets, params = [], []
    if title is not None:
        sets.append("title = ?")
        params.append(title)
    if done is not None:
        sets.append("is_done = ?")
        params.append(int(done))

    if not sets:
        return 0  # nada que actualizar

    params.append(task_id)
    cur = conn.execute(f"UPDATE tasks SET {', '.join(sets)} WHERE id = ?;", params)
    conn.commit()
    return cur.rowcount

def delete_task(conn: sqlite3.Connection, task_id: int) -> int:
    """Elimina una tarea por id. Retorna # de filas eliminadas."""
    cur = conn.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
    conn.commit()
    return cur.rowcount

def get_all_tasks(conn: sqlite3.Connection):
    cur = conn.execute("SELECT id, title, is_done, created_at FROM tasks ORDER BY id;")
    return cur.fetchall()

# --- Ejemplo de uso
#if __name__ == "__main__":
#    conn = get_conn()
#    create_tables(conn)
#
#    # Insertar
#    t1 = insert_task(conn, "Aprender SQLite en Python")
#    print("Tarea creada con id:", t1)
#
#    # Actualizar
#    filas = update_task(conn, t1, done=1)
#    print("Filas actualizadas:", filas)
#
#    # Eliminar
#    filas = delete_task(conn, t1)
#    print("Filas eliminadas:", filas)
#
#    conn.close()
