import sqlite3

DB_FILE = "mars.db"
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
    """Elimina y vuelve a crear las tablas de Rover, Camara y Photos."""
    conn = get_conn()
    try:
        # Eliminar tablas en orden inverso (por las foreign keys)
        conn.execute("DROP TABLE IF EXISTS Photos;")
        conn.execute("DROP TABLE IF EXISTS Camara;")
        conn.execute("DROP TABLE IF EXISTS Rover;")
        
        # Crear tabla Rover
        conn.execute("""
            CREATE TABLE Rover (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL
            );
        """)
        
        # Crear tabla Camara
        conn.execute("""
            CREATE TABLE Camara (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Full_Name TEXT NOT NULL,
                RoverId INTEGER NOT NULL,
                FOREIGN KEY (RoverId) REFERENCES Rover(id)
            );
        """)
        
        # Crear tabla Photos
        conn.execute("""
            CREATE TABLE Photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                CamaraId INTEGER NOT NULL,
                Img_src TEXT NOT NULL,
                Date TEXT NOT NULL,
                FOREIGN KEY (CamaraId) REFERENCES Camara(Id)
            );
        """)
        
        conn.commit()
        print("Las tablas Rover, Camara y Photos se eliminaron y volvieron a crear")
    finally:
        if _should_close_conn(conn):
            conn.close()


# === FUNCIONES PARA ROVER ===

def insert_rover(rover_id: int , name: str):
    """Inserta un rover nuevo y retorna el id generado."""
    conn = get_conn()
    try:
        cur = conn.execute("INSERT INTO Rover (id , Name) VALUES (?,?);", (rover_id , name,))
        conn.commit()
        return cur.lastrowid
    finally:
        if _should_close_conn(conn):
            conn.close()


def update_rover(rover_id: int, name: str = None) -> int:
    """Actualiza el nombre de un rover. Retorna # de filas afectadas."""
    if name is None:
        return 0  # nada que actualizar

    conn = get_conn()
    try:
        cur = conn.execute("UPDATE Rover SET Name = ? WHERE id = ?;", (name, rover_id))
        conn.commit()
        return cur.rowcount
    finally:
        if _should_close_conn(conn):
            conn.close()


def delete_rover(rover_id: int) -> int:
    """Elimina un rover por id. Retorna # de filas eliminadas."""
    conn = get_conn()
    try:
        cur = conn.execute("DELETE FROM Rover WHERE id = ?;", (rover_id,))
        conn.commit()
        return cur.rowcount
    finally:
        if _should_close_conn(conn):
            conn.close()


def get_all_rovers():
    """Obtiene todos los rovers."""
    conn = get_conn()
    try:
        cur = conn.execute("SELECT id, Name FROM Rover ORDER BY id;")
        return cur.fetchall()
    finally:
        if _should_close_conn(conn):
            conn.close()


# === FUNCIONES PARA CAMARA ===

def insert_camara(full_name: str, rover_id: int) -> int:
    """Inserta una cámara nueva y retorna el id generado."""
    conn = get_conn()
    try:
        cur = conn.execute("INSERT INTO Camara (Full_Name, RoverId) VALUES (?, ?);", (full_name, rover_id))
        conn.commit()
        return cur.lastrowid
    finally:
        if _should_close_conn(conn):
            conn.close()


def update_camara(camara_id: int, full_name: str = None, rover_id: int = None) -> int:
    """Actualiza una cámara. Retorna # de filas afectadas."""
    sets, params = [], []
    if full_name is not None:
        sets.append("Full_Name = ?")
        params.append(full_name)
    if rover_id is not None:
        sets.append("RoverId = ?")
        params.append(rover_id)

    if not sets:
        return 0  # nada que actualizar

    params.append(camara_id)
    conn = get_conn()
    try:
        cur = conn.execute(f"UPDATE Camara SET {', '.join(sets)} WHERE Id = ?;", params)
        conn.commit()
        return cur.rowcount
    finally:
        if _should_close_conn(conn):
            conn.close()


def delete_camara(camara_id: int) -> int:
    """Elimina una cámara por id. Retorna # de filas eliminadas."""
    conn = get_conn()
    try:
        cur = conn.execute("DELETE FROM Camara WHERE Id = ?;", (camara_id,))
        conn.commit()
        return cur.rowcount
    finally:
        if _should_close_conn(conn):
            conn.close()


def get_all_camaras():
    """Obtiene todas las cámaras con información del rover."""
    conn = get_conn()
    try:
        cur = conn.execute("""
            SELECT c.Id, c.Full_Name, c.RoverId, r.Name as RoverName 
            FROM Camara c 
            JOIN Rover r ON c.RoverId = r.id 
            ORDER BY c.Id;
        """)
        return cur.fetchall()
    finally:
        if _should_close_conn(conn):
            conn.close()


# === FUNCIONES PARA PHOTOS ===

def insert_photo(camara_id: int, img_src: str, date: str) -> int:
    """Inserta una foto nueva y retorna el id generado."""
    conn = get_conn()
    try:
        cur = conn.execute("INSERT INTO Photos (CamaraId, Img_src, Date) VALUES (?, ?, ?);", (camara_id, img_src, date))
        conn.commit()
        return cur.lastrowid
    finally:
        if _should_close_conn(conn):
            conn.close()


def update_photo(photo_id: int, camara_id: int = None, img_src: str = None, date: str = None) -> int:
    """Actualiza una foto. Retorna # de filas afectadas."""
    sets, params = [], []
    if camara_id is not None:
        sets.append("CamaraId = ?")
        params.append(camara_id)
    if img_src is not None:
        sets.append("Img_src = ?")
        params.append(img_src)
    if date is not None:
        sets.append("Date = ?")
        params.append(date)

    if not sets:
        return 0  # nada que actualizar

    params.append(photo_id)
    conn = get_conn()
    try:
        cur = conn.execute(f"UPDATE Photos SET {', '.join(sets)} WHERE id = ?;", params)
        conn.commit()
        return cur.rowcount
    finally:
        if _should_close_conn(conn):
            conn.close()


def delete_photo(photo_id: int) -> int:
    """Elimina una foto por id. Retorna # de filas eliminadas."""
    conn = get_conn()
    try:
        cur = conn.execute("DELETE FROM Photos WHERE id = ?;", (photo_id,))
        conn.commit()
        return cur.rowcount
    finally:
        if _should_close_conn(conn):
            conn.close()


def get_all_photos():
    """Obtiene todas las fotos con información de la cámara y rover."""
    conn = get_conn()
    try:
        cur = conn.execute("""
            SELECT p.id, p.Img_src, p.Date, c.Full_Name as CamaraName, r.Name as RoverName
            FROM Photos p 
            JOIN Camara c ON p.CamaraId = c.Id 
            JOIN Rover r ON c.RoverId = r.id 
            ORDER BY p.id;
        """)
        return cur.fetchall()
    finally:
        if _should_close_conn(conn):
            conn.close()


def get_photos_by_rover(rover_id: int):
    """Obtiene todas las fotos de un rover específico."""
    conn = get_conn()
    try:
        cur = conn.execute("""
            SELECT p.id, p.Img_src, p.Date, c.Full_Name as CamaraName, r.Name as RoverName
            FROM Photos p 
            JOIN Camara c ON p.CamaraId = c.Id 
            JOIN Rover r ON c.RoverId = r.id 
            WHERE r.id = ?
            ORDER BY p.id;
        """, (rover_id,))
        return cur.fetchall()
    finally:
        if _should_close_conn(conn):
            conn.close()


def get_photos_by_camara(camara_id: int):
    """Obtiene todas las fotos de una cámara específica."""
    conn = get_conn()
    try:
        cur = conn.execute("""
            SELECT p.id, p.Img_src, p.Date, c.Full_Name as CamaraName, r.Name as RoverName
            FROM Photos p 
            JOIN Camara c ON p.CamaraId = c.Id 
            JOIN Rover r ON c.RoverId = r.id 
            WHERE c.Id = ?
            ORDER BY p.id;
        """, (camara_id,))
        return cur.fetchall()
    finally:
        if _should_close_conn(conn):
            conn.close()

