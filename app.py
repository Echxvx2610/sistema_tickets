from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from tools import operaciones_BD
import sqlite3
from datetime import datetime


app = Flask(__name__)

# Configuración de Flask-Login
app.secret_key = 'mi_clave_secreta'  # cifrar clave en produccion
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirige a login si el usuario no está autenticado


# Definir la clase User (usuario)
class User(UserMixin):
    def __init__(self, id, username, role, nombre=None, departamento=None, email=None):
        self.id = id  # ID numérico del usuario en la BD
        self.username = username
        self.role = role
        self.nombre = nombre or username  # Si no hay nombre, usa el username
        self.departamento = departamento
        self.email = email

    def get_id(self):
        return str(self.id)  # Debe retornar un string


# Función para cargar un usuario desde la BD
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, role, departamento, email FROM usuarios WHERE id = ? AND activo = 1', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(
            id=user_data[0], 
            username=user_data[1], 
            role=user_data[2],
            nombre=user_data[1],  # Usando username como nombre
            departamento=user_data[3],
            email=user_data[4]
        )
    return None


# Ruta para el login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verificar credenciales en la base de datos
        conn = sqlite3.connect('tools/sistema_tickets.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, role, departamento, email FROM usuarios WHERE username = ? AND password = ? AND activo = 1', 
                      (username, password))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            user = User(
                id=user_data[0], 
                username=user_data[1], 
                role=user_data[2],
                nombre=user_data[1],  # Usando username como nombre
                departamento=user_data[3],
                email=user_data[4]
            )
            login_user(user)  # Inicia la sesión del usuario
            return redirect(url_for('index'))  # Redirige a la página principal
        else:
            error_message = 'Usuario o contraseña incorrectos'
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')


# Ruta para la página principal (index) - Acceso restringido por tipo de usuario
@app.route('/index')
@login_required
def index():
    # Obtener los tickets desde la base de datos
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()

    # Consulta adaptada a la nueva estructura
    cursor.execute(''' 
    SELECT t.id, t.titulo, t.descripcion, t.estado, t.prioridad, 
           t.fecha_creacion, t.fecha_actualizacion, t.fecha_cierre, 
           t.area, t.ubicacion, t.categoria, t.tipo_servicio,
           c.username AS creador_nombre, s.username AS soporte_nombre
    FROM tickets t
    LEFT JOIN usuarios c ON t.creador_id = c.id
    LEFT JOIN usuarios s ON t.soporte_id = s.id
    ORDER BY 
        CASE 
            WHEN t.prioridad = 'Alta' THEN 1
            WHEN t.prioridad = 'Media' THEN 2
            WHEN t.prioridad = 'Baja' THEN 3
            ELSE 4
        END,
        t.fecha_creacion DESC
    ''')

    # Obtener los resultados y convertir cada fila en un diccionario
    tickets = []
    for row in cursor.fetchall():
        fecha_creacion = datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S') if row[5] else None
        fecha_actualizacion = datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S') if row[6] else None
        fecha_cierre = datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S') if row[7] else None
        
        ticket = {
            'id': row[0],
            'titulo': row[1],
            'descripcion': row[2],
            'estado': row[3],
            'prioridad': row[4],
            'fecha_creacion': fecha_creacion,
            'fecha_actualizacion': fecha_actualizacion,
            'fecha_cierre': fecha_cierre,
            'area': row[8],
            'ubicacion': row[9],
            'categoria': row[10],
            'tipo_servicio': row[11],
            'creador_nombre': row[12],
            'soporte_nombre': row[13]
        }

        tickets.append(ticket)

    # Obtener tickets específicos según el rol del usuario
    user_role = current_user.role
    user_id = current_user.id
    
    if user_role == 'Administrador':
        # Administrador ve todos los tickets (ya obtenidos)
        pass
    elif user_role == 'Soporte':
        # Personal de soporte ve tickets asignados a él y tickets sin asignar
        cursor.execute('''
        SELECT t.id, t.titulo, t.descripcion, t.estado, t.prioridad, 
               t.fecha_creacion, t.fecha_actualizacion, t.fecha_cierre, 
               t.area, t.ubicacion, t.categoria, t.tipo_servicio,
               c.username AS creador_nombre, s.username AS soporte_nombre
        FROM tickets t
        LEFT JOIN usuarios c ON t.creador_id = c.id
        LEFT JOIN usuarios s ON t.soporte_id = s.id
        WHERE t.soporte_id = ? OR t.soporte_id IS NULL
        ORDER BY 
            CASE 
                WHEN t.prioridad = 'Alta' THEN 1
                WHEN t.prioridad = 'Media' THEN 2
                WHEN t.prioridad = 'Baja' THEN 3
                ELSE 4
            END,
            t.fecha_creacion DESC
        ''', (user_id,))
        
        tickets = []
        for row in cursor.fetchall():
            fecha_creacion = datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S') if row[5] else None
            fecha_actualizacion = datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S') if row[6] else None
            fecha_cierre = datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S') if row[7] else None
            
            ticket = {
                'id': row[0],
                'titulo': row[1],
                'descripcion': row[2],
                'estado': row[3],
                'prioridad': row[4],
                'fecha_creacion': fecha_creacion,
                'fecha_actualizacion': fecha_actualizacion,
                'fecha_cierre': fecha_cierre,
                'area': row[8],
                'ubicacion': row[9],
                'categoria': row[10],
                'tipo_servicio': row[11],
                'creador_nombre': row[12],
                'soporte_nombre': row[13]
            }
            
            tickets.append(ticket)
            
    elif user_role in ['Produccion', 'Oficina']:
        # Usuarios de producción u oficina solo ven sus propios tickets
        cursor.execute('''
        SELECT t.id, t.titulo, t.descripcion, t.estado, t.prioridad, 
               t.fecha_creacion, t.fecha_actualizacion, t.fecha_cierre, 
               t.area, t.ubicacion, t.categoria, t.tipo_servicio,
               c.username AS creador_nombre, s.username AS soporte_nombre
        FROM tickets t
        LEFT JOIN usuarios c ON t.creador_id = c.id
        LEFT JOIN usuarios s ON t.soporte_id = s.id
        WHERE t.creador_id = ?
        ORDER BY t.fecha_creacion DESC
        ''', (user_id,))
        
        tickets = []
        for row in cursor.fetchall():
            fecha_creacion = datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S') if row[5] else None
            fecha_actualizacion = datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S') if row[6] else None
            fecha_cierre = datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S') if row[7] else None
            
            ticket = {
                'id': row[0],
                'titulo': row[1],
                'descripcion': row[2],
                'estado': row[3],
                'prioridad': row[4],
                'fecha_creacion': fecha_creacion,
                'fecha_actualizacion': fecha_actualizacion,
                'fecha_cierre': fecha_cierre,
                'area': row[8],
                'ubicacion': row[9],
                'categoria': row[10],
                'tipo_servicio': row[11],
                'creador_nombre': row[12],
                'soporte_nombre': row[13]
            }
            
            tickets.append(ticket)

    conn.close()

    # Renderizar plantilla según el rol del usuario
    if user_role == 'Administrador':
        return render_template('view_administrador/index.html', tickets=tickets)
    elif user_role == 'Soporte':
        return render_template('view_soporte/index.html', tickets=tickets)
    elif user_role in ['Produccion', 'Oficina']:
        return render_template('view_produccion/index.html', tickets=tickets)

    # Si no coincide con ningún rol específico, redirigir a una página por defecto
    return render_template('index.html', tickets=tickets)


# Ruta para crear un nuevo ticket
@app.route('/crear_ticket', methods=['GET', 'POST'])
@login_required
def crear_ticket():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        tipo_servicio = request.form['tipo_servicio']
        categoria = request.form['categoria']
        prioridad = request.form['prioridad']
        area = request.form['area'] if 'area' in request.form else current_user.role
        ubicacion = request.form['ubicacion'] if 'ubicacion' in request.form else current_user.departamento
        
        # Estado siempre es "Pendiente" al crear un nuevo ticket
        estado = "Pendiente"
        
        # El creador es el usuario actual
        creador_id = current_user.id
        
        # Sin técnico asignado inicialmente
        soporte_id = None
        
        conn = sqlite3.connect('tools/sistema_tickets.db')
        cursor = conn.cursor()
        
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO tickets (titulo, descripcion, estado, prioridad, creador_id, soporte_id, 
                              tipo_servicio, categoria, fecha_creacion, fecha_actualizacion, 
                              fecha_cierre, area, ubicacion) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (titulo, descripcion, estado, prioridad, creador_id, soporte_id, 
              tipo_servicio, categoria, fecha_actual, fecha_actual, None, area, ubicacion))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
        
    return render_template('crear_ticket.html')


# Ruta para ver los detalles de un ticket
@app.route('/ticket/<int:ticket_id>')
@login_required
def ver_ticket(ticket_id):
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    
    # Obtener información del ticket
    cursor.execute('''
    SELECT t.*, 
           c.username AS creador_nombre, 
           s.username AS soporte_nombre
    FROM tickets t
    LEFT JOIN usuarios c ON t.creador_id = c.id
    LEFT JOIN usuarios s ON t.soporte_id = s.id
    WHERE t.id = ?
    ''', (ticket_id,))
    
    ticket_data = cursor.fetchone()
    
    if not ticket_data:
        conn.close()
        return redirect(url_for('index'))
    
    # Convertir a diccionario
    ticket = {
        'id': ticket_data[0],
        'titulo': ticket_data[1],
        'descripcion': ticket_data[2],
        'estado': ticket_data[3],
        'prioridad': ticket_data[4],
        'creador_id': ticket_data[5],
        'soporte_id': ticket_data[6],
        'tipo_servicio': ticket_data[7],
        'categoria': ticket_data[8],
        'fecha_creacion': ticket_data[9],
        'fecha_actualizacion': ticket_data[10],
        'fecha_cierre': ticket_data[11],
        'area': ticket_data[12],
        'ubicacion': ticket_data[13],
        'creador_nombre': ticket_data[14],
        'soporte_nombre': ticket_data[15]
    }
    
    # Obtener comentarios del ticket
    cursor.execute('''
    SELECT c.*, u.username
    FROM comentarios c
    JOIN usuarios u ON c.usuario_id = u.id
    WHERE c.ticket_id = ?
    ORDER BY c.fecha ASC
    ''', (ticket_id,))
    
    comentarios = []
    for row in cursor.fetchall():
        comentario = {
            'id': row[0],
            'ticket_id': row[1],
            'usuario_id': row[2],
            'contenido': row[3],
            'fecha': row[4],
            'username': row[5]
        }
        comentarios.append(comentario)
    
    # Obtener la lista de técnicos de soporte para asignar
    cursor.execute('SELECT id, username FROM usuarios WHERE role = "Soporte" AND activo = 1')
    tecnicos = cursor.fetchall()
    
    conn.close()
    
    return render_template('ver_ticket.html', ticket=ticket, comentarios=comentarios, tecnicos=tecnicos)


# Ruta para añadir un comentario a un ticket
@app.route('/ticket/<int:ticket_id>/comentar', methods=['POST'])
@login_required
def comentar_ticket(ticket_id):
    contenido = request.form['contenido']
    
    if contenido.strip():  # Verificar que el comentario no esté vacío
        conn = sqlite3.connect('tools/sistema_tickets.db')
        cursor = conn.cursor()
        
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO comentarios (ticket_id, usuario_id, contenido, fecha)
            VALUES (?, ?, ?, ?)
        ''', (ticket_id, current_user.id, contenido, fecha_actual))
        
        # Actualizar la fecha de actualización del ticket
        cursor.execute('''
            UPDATE tickets 
            SET fecha_actualizacion = ? 
            WHERE id = ?
        ''', (fecha_actual, ticket_id))
        
        conn.commit()
        conn.close()
    
    return redirect(url_for('ver_ticket', ticket_id=ticket_id))


# Ruta para actualizar el estado de un ticket
@app.route('/ticket/<int:ticket_id>/actualizar', methods=['POST'])
@login_required
def actualizar_ticket(ticket_id):
    # Verificar si el usuario tiene permisos (administrador o soporte)
    if current_user.role not in ['Administrador', 'Soporte']:
        return redirect(url_for('index'))
    
    estado = request.form['estado']
    soporte_id = request.form.get('soporte_id')
    
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()
    
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Si el estado cambia a "Completado", actualizar fecha de cierre
    if estado == 'Completado':
        cursor.execute('''
            UPDATE tickets 
            SET estado = ?, soporte_id = ?, fecha_actualizacion = ?, fecha_cierre = ?
            WHERE id = ?
        ''', (estado, soporte_id, fecha_actual, fecha_actual, ticket_id))
    else:
        cursor.execute('''
            UPDATE tickets 
            SET estado = ?, soporte_id = ?, fecha_actualizacion = ?, fecha_cierre = NULL
            WHERE id = ?
        ''', (estado, soporte_id, fecha_actual, ticket_id))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('ver_ticket', ticket_id=ticket_id))



# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@app.route('/tickets')
def tickets():
    return render_template('tickets.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
