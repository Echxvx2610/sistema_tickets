import sqlite3
from datetime import datetime

# Crear BD para sistema de tickets
def create_database():
    """
    Modelos de la BD:
    - Usuario:
        Atributos:
            - id
            - username
            - password
            - role (Administrador, Soporte, Produccion, Oficina)
            - departamento
            - email
            - activo
        Métodos:
            - __init__(self, id, username, password, role, departamento, email, activo)
            - __str__(self)
            - __repr__(self)
            - getter y setter de cada atributo
            
    - Ticket:
        Atributos:
            - id
            - titulo
            - descripcion
            - estado (Pendiente, En Proceso, Completado, Cancelado)
            - prioridad (Alta, Media, Baja)
            - creador_id (usuario que creó el ticket)
            - soporte_id (usuario de soporte asignado para solucionar el ticket)
            - tipo_servicio
            - categoria (Hardware, Software, Red, Otro)
            - fecha_creacion
            - fecha_actualizacion
            - fecha_cierre
            - area (Produccion, Oficina)
            - ubicacion
        Métodos:
            - __init__(self, id, titulo, descripcion, estado, prioridad, creador_id, soporte_id, tipo_servicio, categoria, fecha_creacion, fecha_actualizacion, fecha_cierre, area, ubicacion)
            - __str__(self)
            - __repr__(self)
            - getter y setter de cada atributo
            
    - Comentario:
        Atributos:
            - id
            - ticket_id
            - usuario_id
            - contenido
            - fecha
        Métodos:
            - __init__(self, id, ticket_id, usuario_id, contenido, fecha)
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
            role TEXT NOT NULL,
            departamento TEXT,
            email TEXT,
            activo INTEGER DEFAULT 1
        )
    ''')

    # Crear tabla de tickets con las columnas necesarias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            estado TEXT NOT NULL,
            prioridad TEXT NOT NULL,
            creador_id INTEGER NOT NULL,
            soporte_id INTEGER,
            tipo_servicio TEXT,
            categoria TEXT,
            fecha_creacion TEXT NOT NULL,
            fecha_actualizacion TEXT,
            fecha_cierre TEXT,
            area TEXT NOT NULL,
            ubicacion TEXT,
            FOREIGN KEY (creador_id) REFERENCES usuarios(id),
            FOREIGN KEY (soporte_id) REFERENCES usuarios(id)
        )
    ''')
    
    # Crear tabla de comentarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            contenido TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
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
            'id': row[0],
            'username': row[1],
            'password': row[2],
            'role': row[3],
            'departamento': row[4],
            'email': row[5],
            'activo': row[6]
        }
        users.append(user)

    conn.close()
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
            'prioridad': row[4],
            'creador_id': row[5],
            'soporte_id': row[6],
            'tipo_servicio': row[7],
            'categoria': row[8],
            'fecha_creacion': row[9],
            'fecha_actualizacion': row[10],
            'fecha_cierre': row[11],
            'area': row[12],
            'ubicacion': row[13]
        }
        tickets.append(ticket)
    
    conn.close()
    return tickets

def get_list_comentarios():
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comentarios')
    rows = cursor.fetchall()
    
    comentarios = []
    for row in rows:
        comentario = {
            'id': row[0],
            'ticket_id': row[1],
            'usuario_id': row[2],
            'contenido': row[3],
            'fecha': row[4]
        }
        comentarios.append(comentario)
    
    conn.close()
    return comentarios

# Operaciones CRUD para usuarios
def register_user(username, password, role, departamento=None, email=None, activo=1):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (username, password, role, departamento, email, activo) VALUES (?, ?, ?, ?, ?, ?)', 
                  (username, password, role, departamento, email, activo))
    conn.commit()
    conn.close()

def update_user(user_id, username, password, role, departamento=None, email=None, activo=1):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET username = ?, password = ?, role = ?, departamento = ?, email = ?, activo = ? WHERE id = ?', 
                  (username, password, role, departamento, email, activo, user_id))
    conn.commit()
    conn.close()
  
def delete_user(user_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

def deactivate_user(user_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET activo = 0 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_info_user(user_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        user = {
            'id': row[0],
            'username': row[1],
            'password': row[2],
            'role': row[3],
            'departamento': row[4],
            'email': row[5],
            'activo': row[6]
        }
        return user
    return None

# Operaciones CRUD para tickets
def register_ticket(titulo, descripcion, estado, prioridad, creador_id, soporte_id, tipo_servicio, categoria, area, ubicacion):
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tickets (titulo, descripcion, estado, prioridad, creador_id, soporte_id, 
                            tipo_servicio, categoria, fecha_creacion, fecha_actualizacion, 
                            fecha_cierre, area, ubicacion) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (titulo, descripcion, estado, prioridad, creador_id, soporte_id, tipo_servicio, 
         categoria, fecha_actual, fecha_actual, None, area, ubicacion))
    ticket_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return ticket_id

def update_ticket(ticket_id, titulo, descripcion, estado, prioridad, soporte_id, tipo_servicio, categoria, area, ubicacion):
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    
    # Si el estado es "Completado", actualizar la fecha de cierre
    fecha_cierre = None
    if estado == 'Completado':
        fecha_cierre = fecha_actual
    
    cursor.execute('''
        UPDATE tickets 
        SET titulo = ?, descripcion = ?, estado = ?, prioridad = ?, soporte_id = ?, 
            tipo_servicio = ?, categoria = ?, fecha_actualizacion = ?, fecha_cierre = ?, 
            area = ?, ubicacion = ? 
        WHERE id = ?
    ''', (titulo, descripcion, estado, prioridad, soporte_id, tipo_servicio, categoria, 
          fecha_actual, fecha_cierre, area, ubicacion, ticket_id))
    conn.commit()
    conn.close()
    
def delete_ticket(ticket_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    # Primero eliminar comentarios asociados
    cursor.execute('DELETE FROM comentarios WHERE ticket_id = ?', (ticket_id,))
    # Luego eliminar el ticket
    cursor.execute('DELETE FROM tickets WHERE id = ?', (ticket_id,))
    conn.commit()
    conn.close()

def get_info_ticket(ticket_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        ticket = {
            'id': row[0],
            'titulo': row[1],
            'descripcion': row[2],
            'estado': row[3],
            'prioridad': row[4],
            'creador_id': row[5],
            'soporte_id': row[6],
            'tipo_servicio': row[7],
            'categoria': row[8],
            'fecha_creacion': row[9],
            'fecha_actualizacion': row[10],
            'fecha_cierre': row[11],
            'area': row[12],
            'ubicacion': row[13]
        }
        return ticket
    return None

# Operaciones CRUD para comentarios
def add_comentario(ticket_id, usuario_id, contenido):
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO comentarios (ticket_id, usuario_id, contenido, fecha)
        VALUES (?, ?, ?, ?)
    ''', (ticket_id, usuario_id, contenido, fecha_actual))
    conn.commit()
    conn.close()

def get_comentarios_by_ticket(ticket_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.*, u.username 
        FROM comentarios c
        JOIN usuarios u ON c.usuario_id = u.id
        WHERE c.ticket_id = ?
        ORDER BY c.fecha ASC
    ''', (ticket_id,))
    rows = cursor.fetchall()
    
    comentarios = []
    for row in rows:
        comentario = {
            'id': row[0],
            'ticket_id': row[1],
            'usuario_id': row[2],
            'contenido': row[3],
            'fecha': row[4],
            'username': row[5]
        }
        comentarios.append(comentario)
    
    conn.close()
    return comentarios

# Funciones auxiliares
def get_username_by_id(user_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM usuarios WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_tickets_by_creador(creador_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets WHERE creador_id = ? ORDER BY fecha_creacion DESC', (creador_id,))
    rows = cursor.fetchall()
    
    tickets = []
    for row in rows:
        ticket = {
            'id': row[0],
            'titulo': row[1],
            'descripcion': row[2],
            'estado': row[3],
            'prioridad': row[4],
            'creador_id': row[5],
            'soporte_id': row[6],
            'tipo_servicio': row[7],
            'categoria': row[8],
            'fecha_creacion': row[9],
            'fecha_actualizacion': row[10],
            'fecha_cierre': row[11],
            'area': row[12],
            'ubicacion': row[13]
        }
        tickets.append(ticket)
    
    conn.close()
    return tickets

def get_tickets_by_soporte(soporte_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets WHERE soporte_id = ? ORDER BY prioridad, fecha_creacion DESC', (soporte_id,))
    rows = cursor.fetchall()
    
    tickets = []
    for row in rows:
        ticket = {
            'id': row[0],
            'titulo': row[1],
            'descripcion': row[2],
            'estado': row[3],
            'prioridad': row[4],
            'creador_id': row[5],
            'soporte_id': row[6],
            'tipo_servicio': row[7],
            'categoria': row[8],
            'fecha_creacion': row[9],
            'fecha_actualizacion': row[10],
            'fecha_cierre': row[11],
            'area': row[12],
            'ubicacion': row[13]
        }
        tickets.append(ticket)
    
    conn.close()
    return tickets

def get_tickets_by_area(area):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets WHERE area = ? ORDER BY fecha_creacion DESC', (area,))
    rows = cursor.fetchall()
    
    tickets = []
    for row in rows:
        ticket = {
            'id': row[0],
            'titulo': row[1],
            'descripcion': row[2],
            'estado': row[3],
            'prioridad': row[4],
            'creador_id': row[5],
            'soporte_id': row[6],
            'tipo_servicio': row[7],
            'categoria': row[8],
            'fecha_creacion': row[9],
            'fecha_actualizacion': row[10],
            'fecha_cierre': row[11],
            'area': row[12],
            'ubicacion': row[13]
        }
        tickets.append(ticket)
    
    conn.close()
    return tickets

# Función para inicializar la base de datos
def initialize_database():
    create_database()
    # Insertar usuario administrador por defecto
    register_user('admin', 'admin123', 'Administrador', 'Sistemas', 'admin@empresa.com')
    print("Base de datos inicializada con éxito.")

# Funciones para insertar datos de prueba
def insertar_usuarios_prueba():
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()

    # Datos de prueba para insertar en la tabla usuarios
    usuarios_prueba = [
        ('admin1', 'pass123', 'Administrador', 'Sistemas', 'admin1@empresa.com', 1),
        ('soporte1', 'pass123', 'Soporte', 'IT', 'soporte1@empresa.com', 1),
        ('soporte2', 'pass123', 'Soporte', 'IT', 'soporte2@empresa.com', 1),
        ('prod1', 'pass123', 'Produccion', 'Planta 1', 'prod1@empresa.com', 1),
        ('prod2', 'pass123', 'Produccion', 'Planta 2', 'prod2@empresa.com', 1),
        ('ofic1', 'pass123', 'Oficina', 'Administración', 'ofic1@empresa.com', 1),
        ('ofic2', 'pass123', 'Oficina', 'Contabilidad', 'ofic2@empresa.com', 1),
        ('ofic3', 'pass123', 'Oficina', 'RRHH', 'ofic3@empresa.com', 1)
    ]

    # Insertar los registros de prueba en la tabla usuarios
    cursor.executemany('''
        INSERT INTO usuarios (username, password, role, departamento, email, activo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', usuarios_prueba)

    conn.commit()
    conn.close()
    print("Usuarios de prueba insertados con éxito.")

def insertar_tickets_prueba():
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Datos de prueba para insertar en la tabla tickets
    tickets_prueba = [
        ('PC no enciende', 'Mi computadora no enciende desde esta mañana', 'Pendiente', 'Alta', 4, 2, 'Hardware', 'Hardware', fecha_actual, fecha_actual, None, 'Produccion', 'Planta 1 - Línea A'),
        ('Problema con impresora', 'La impresora de oficina no imprime documentos PDF', 'En Proceso', 'Media', 6, 3, 'Hardware', 'Hardware', fecha_actual, fecha_actual, None, 'Oficina', 'Administración'),
        ('Solicitud de nuevo software', 'Necesito instalación de programa de diseño', 'Pendiente', 'Baja', 7, None, 'Software', 'Software', fecha_actual, fecha_actual, None, 'Oficina', 'Contabilidad'),
        ('Error en sistema ERP', 'No puedo acceder al módulo de inventarios', 'En Proceso', 'Alta', 5, 2, 'Software', 'Software', fecha_actual, fecha_actual, None, 'Produccion', 'Planta 2'),
        ('Configuración de correo', 'Necesito configurar mi correo en el celular', 'Completado', 'Baja', 8, 3, 'Configuración', 'Software', fecha_actual, fecha_actual, fecha_actual, 'Oficina', 'RRHH'),
        ('Problemas de conexión', 'No tengo acceso a internet desde mi puesto', 'Pendiente', 'Media', 6, None, 'Red', 'Red', fecha_actual, fecha_actual, None, 'Oficina', 'Administración')
    ]

    # Insertar los registros de prueba en la tabla tickets
    cursor.executemany('''
        INSERT INTO tickets (titulo, descripcion, estado, prioridad, creador_id, soporte_id, 
                           tipo_servicio, categoria, fecha_creacion, fecha_actualizacion, 
                           fecha_cierre, area, ubicacion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tickets_prueba)

    conn.commit()
    conn.close()
    print("Tickets de prueba insertados con éxito.")

def insertar_comentarios_prueba():
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Datos de prueba para insertar en la tabla comentarios
    comentarios_prueba = [
        (1, 2, 'Revisaré tu equipo esta tarde', fecha_actual),
        (1, 4, 'Gracias, estaré esperando', fecha_actual),
        (2, 3, 'Ya revisé la impresora, parece ser un problema de controladores', fecha_actual),
        (2, 6, '¿Cuándo estará solucionado?', fecha_actual),
        (2, 3, 'Mañana instalaré los controladores actualizados', fecha_actual),
        (4, 2, 'Estoy trabajando en el problema, parece ser un error de permisos', fecha_actual),
        (5, 3, 'Configuración completada, por favor verifica tu correo', fecha_actual),
        (5, 8, 'Funciona perfectamente, gracias', fecha_actual)
    ]

    # Insertar los registros de prueba en la tabla comentarios
    cursor.executemany('''
        INSERT INTO comentarios (ticket_id, usuario_id, contenido, fecha)
        VALUES (?, ?, ?, ?)
    ''', comentarios_prueba)

    conn.commit()
    conn.close()
    print("Comentarios de prueba insertados con éxito.")

# Función para inicializar con datos de prueba
def initialize_with_test_data():
    create_database()
    insertar_usuarios_prueba()
    insertar_tickets_prueba()
    insertar_comentarios_prueba()
    print("Base de datos inicializada con datos de prueba.")

# Para ejecutar la inicialización
# initialize_database()  # Solo estructura y admin
# initialize_with_test_data()  # Con datos de prueba