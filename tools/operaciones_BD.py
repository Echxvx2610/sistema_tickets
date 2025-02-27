import sqlite3
from datetime import datetime


# crear BD para sistema de tickets
def create_database():
    """
        Modelos de la BD:
        - Usuario:
            Atributos:
                - id
                - username
                - password
                - role
            Métodos:
                - __init__(self, id, username, password, role)
                - __str__(self)
                - __repr__(self)
                - getter y setter de cada atributo
                
        - Ticket:
            Atributos:
                - id
                - titulo
                - descripcion
                - estado
                - usuario_id (usuario que creó el ticket)
                - tecnico_id (usuario que está asignado para solucionar el ticket, puede ser null)
                - tipo_servicio
                - turno
                - fecha
                - area
                - celda
            Métodos:
                - __init__(self, id, titulo, descripcion, estado, usuario_id, tecnico_id, tipo_servicio, turno, fecha, area, celda)
                - __str__(self)
                - __repr__(self)
                - getter y setter de cada atributo
    """
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()

    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Crear tabla de tickets con las columnas necesarias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            estado TEXT NOT NULL,
            usuario_id INTEGER NOT NULL,  -- Relación con el usuario que crea el ticket
            tecnico_id INTEGER,  -- Relación con el técnico asignado
            tipo_servicio TEXT,
            turno TEXT,
            fecha TEXT,  -- Guarda la fecha como texto en formato 'YYYY-MM-DD HH:MM'
            area TEXT,
            celda TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (tecnico_id) REFERENCES usuarios(id)  -- Relación con el técnico
        )
    ''')

    conn.commit()
    conn.close()


def get_list_users():
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    rows = cursor.fetchall()

    # Convertir las filas a diccionarios
    users = []
    for row in rows:
        user = {
            'id': row[0],  # Asumiendo que 'id' está en la primera columna
            'username': row[1],  # 'username' en la segunda columna
            'password': row[2]   # 'password' en la tercera columna
        }
        users.append(user)

    return users

def get_list_tickets():
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets')
    rows = cursor.fetchall()
    
    # Convertir filas a diccionarios con nombres de columnas
    tickets = []
    for row in rows:
        ticket = {
            'id': row[0],
            'titulo': row[1],
            'descripcion': row[2],
            'estado': row[3],
            'usuario_id': row[4]
        }
        tickets.append(ticket)
    
    return tickets

# operaciones CRUD
def register_user(username, password, role):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)', (username, password, role))
    conn.commit()
    conn.close()

def update_user(user_id, username, password, role):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET username = ?, password = ?, role = ? WHERE id = ?', (username, password, role, user_id))
    conn.commit()
    conn.close()
  
def delete_user(user_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_info_user(user_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def register_ticket(titulo, descripcion, estado, usuario_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tickets (titulo, descripcion, estado, usuario_id) VALUES (?, ?, ?, ?)', (titulo, descripcion, estado, usuario_id))
    conn.commit()
    conn.close()

def update_ticket(ticket_id, titulo, descripcion, estado, usuario_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tickets SET titulo = ?, descripcion = ?, estado = ?, usuario_id = ? WHERE id = ?', (titulo, descripcion, estado, usuario_id, ticket_id))
    conn.commit()
    conn.close()
    
def delete_ticket(ticket_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tickets WHERE id = ?', (ticket_id,))
    conn.commit()
    conn.close()

def get_info_ticket(ticket_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_element_by_id(table, id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table} WHERE id = ?', (id,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_username_by_ticket(user_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    
    # Consulta para obtener el nombre del usuario por su ID
    cursor.execute('''
        SELECT username
        FROM usuarios
        WHERE id = ?
    ''', (user_id,))
    
    # Obtener el resultado
    user = cursor.fetchone()
    
    if user:
        return user[0]  # Retorna el nombre de usuario
    else:
        return None  # No se encontró el usuario
    
    conn.close()

def insertar_registros_prueba():
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()

    # Datos de prueba para insertar en la tabla tickets
    tickets_prueba = [
        ('Problema A', 'Descripción del problema A', 'Pendiente', 1, None, 'Servicio A', 'Turno A', '2025-02-27 10:00', 'Área 1', 'Celda 1'),
        ('Problema B', 'Descripción del problema B', 'En Proceso', 2, 1, 'Servicio B', 'Turno B', '2025-02-27 11:00', 'Área 2', 'Celda 2'),
        ('Problema C', 'Descripción del problema C', 'Completado', 1, 2, 'Servicio C', 'Turno C', '2025-02-27 12:00', 'Área 3', 'Celda 3'),
        ('Problema D', 'Descripción del problema D', 'Pendiente', 3, None, 'Servicio D', 'Turno D', '2025-02-27 13:00', 'Área 4', 'Celda 4'),
        ('Problema E', 'Descripción del problema E', 'En Proceso', 2, 3, 'Servicio E', 'Turno E', '2025-02-27 14:00', 'Área 5', 'Celda 5'),
        ('Problema F', 'Descripción del problema F', 'Pendiente', 1, None, 'Servicio F', 'Turno F', '2025-02-27 15:00', 'Área 6', 'Celda 6'),
        ('Problema G', 'Descripción del problema G', 'Completado', 3, 1, 'Servicio G', 'Turno G', '2025-02-27 16:00', 'Área 7', 'Celda 7'),
        ('Problema H', 'Descripción del problema H', 'Pendiente', 2, None, 'Servicio H', 'Turno H', '2025-02-27 17:00', 'Área 8', 'Celda 8'),
        ('Problema I', 'Descripción del problema I', 'En Proceso', 1, 2, 'Servicio I', 'Turno I', '2025-02-27 18:00', 'Área 9', 'Celda 9'),
        ('Problema J', 'Descripción del problema J', 'Completado', 3, 1, 'Servicio J', 'Turno J', '2025-02-27 19:00', 'Área 10', 'Celda 10')
    ]

    # Insertar los registros de prueba en la tabla tickets
    cursor.executemany('''
        INSERT INTO tickets (titulo, descripcion, estado, usuario_id, tecnico_id, tipo_servicio, turno, fecha, area, celda)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tickets_prueba)

    conn.commit()
    conn.close()
    print("Registros de prueba insertados con éxito.")

def insertar_usuarios_prueba():
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()

    # Datos de prueba para insertar en la tabla usuarios
    usuarios_prueba = [
        ('usuario1', 'password1', 'admin'),
        ('usuario2', 'password2', 'usuario'),
        ('usuario3', 'password3', 'tecnico'),
        ('usuario4', 'password4', 'usuario'),
        ('usuario5', 'password5', 'admin'),
        ('usuario6', 'password6', 'tecnico'),
        ('usuario7', 'password7', 'usuario'),
        ('usuario8', 'password8', 'usuario'),
        ('usuario9', 'password9', 'tecnico'),
        ('usuario10', 'password10', 'admin')
    ]

    # Insertar los registros de prueba en la tabla usuarios
    cursor.executemany('''
        INSERT INTO usuarios (username, password, role)
        VALUES (?, ?, ?)
    ''', usuarios_prueba)

    conn.commit()
    conn.close()
    print("Usuarios de prueba insertados con éxito.")


# create_database()
# insertar_usuarios_prueba()
# insertar_registros_prueba()