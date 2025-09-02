import sqlite3

import sqlite3

DB_FILE = "todo.db"
_test_conn: sqlite3.Connection | None = None  # conexión de prueba (si está seteada)


def get_conn(db_file: str = DB_FILE) -> sqlite3.Connection:
    """Devuelve la conexión: la real o la inyectada en test."""
    global _test_conn
    if _test_conn is not None:
        return _test_conn
    conn = sqlite3.connect(db_file)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def override_conn_for_tests(conn: sqlite3.Connection | None) -> None:
    """Permite inyectar una conexión (ej. en tests con :memory:)."""
    global _test_conn
    _test_conn = conn


def _should_close_conn(conn: sqlite3.Connection) -> bool:
    """Indica si el wrapper debe cerrar la conexión."""
    return _test_conn is None or conn is not _test_conn


def create_tables() -> None:
    """Elimina y vuelve a crear la tabla de tareas."""
    conn = get_conn()
    try:
        conn.execute("DROP TABLE IF EXISTS tasks;")
        conn.execute("""
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                is_done INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
        """)
        conn.commit()
        print("La tabla tasks se eliminó y volvió a crear")
    finally:
        if _should_close_conn(conn):
            conn.close()


def insert_task(title: str) -> int:
    """Inserta una tarea nueva y retorna el id generado."""
    conn = get_conn()
    try:
        cur = conn.execute("INSERT INTO tasks (title) VALUES (?);", (title,))
        conn.commit()
        return cur.lastrowid
    finally:
        if _should_close_conn(conn):
            conn.close()


def update_task(task_id: int, title: str = None, done: int = None) -> int:
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
    conn = get_conn()
    try:
        cur = conn.execute(f"UPDATE tasks SET {', '.join(sets)} WHERE id = ?;", params)
        conn.commit()
        return cur.rowcount
    finally:
        if _should_close_conn(conn):
            conn.close()


def delete_task(task_id: int) -> int:
    """Elimina una tarea por id. Retorna # de filas eliminadas."""
    conn = get_conn()
    try:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
        conn.commit()
        return cur.rowcount
    finally:
        if _should_close_conn(conn):
            conn.close()


def get_all_tasks():
    """Obtiene todas las tareas."""
    conn = get_conn()
    try:
        cur = conn.execute("SELECT id, title, is_done, created_at FROM tasks ORDER BY id;")
        return cur.fetchall()
    finally:
        if _should_close_conn(conn):
            conn.close()

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
