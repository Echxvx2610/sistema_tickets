import sqlite3

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
            Metodos:
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
                - usuario_id
            Metodos:
                - __init__(self, id, titulo, descripcion, estado, usuario_id)
                - __str__(self)
                - __repr__(self)
                - getter y setter de cada atributo
        """
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            estado TEXT NOT NULL,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

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
