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

# Datos de usuario Dummy con roles
USER_CREDENTIALS = {
    'admin': {'password': 'admin123', 'role': 'administrador', 'nombre': 'Administrador'},
    'soporte1': {'password': 'soporte123', 'role': 'soporte', 'nombre': 'Soporte 1'},
    'produccion1': {'password': 'produccion123', 'role': 'produccion', 'nombre': 'Producción 1'}
}


# Definir la clase User (usuario)
class User(UserMixin):
    def __init__(self, username, role, nombre=None):
        self.id = username
        self.role = role
        self.nombre = nombre or username  # Si no tienes un nombre, usa el username por defecto

    def get_id(self):
        return self.id


# Función para cargar un usuario
@login_manager.user_loader
def load_user(username):
    if username in USER_CREDENTIALS:
        role = USER_CREDENTIALS[username]['role']
        nombre = USER_CREDENTIALS[username]['nombre']
        return User(username, role, nombre)
    return None


# Ruta para el login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verifica si las credenciales son correctas
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username]['password'] == password:
            user = User(username, USER_CREDENTIALS[username]['role'])
            login_user(user)  # Inicia la sesión del usuario
            return redirect(url_for('index'))  # Redirige a la página principal si el login es exitoso
        else:
            error_message = 'Usuario o contraseña incorrectos'  # Mensaje de error
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')

# Ruta para la página principal (index) - Acceso restringido por tipo de usuario
@app.route('/index')
@login_required
def index():
    # Obtener los tickets desde la base de datos
    conn = sqlite3.connect('tools/sistema_tickets.db')
    cursor = conn.cursor()

    cursor.execute(''' 
        SELECT t.id, t.titulo, t.descripcion, t.estado, t.turno, t.fecha, t.area, t.celda,
               t.usuario_id, t.tecnico_id, t.tipo_servicio
        FROM tickets t
    ''')

    # Obtener los resultados y convertir cada fila en un diccionario
    tickets = []
    for row in cursor.fetchall():
        fecha = datetime.strptime(row[5], '%Y-%m-%d %H:%M') if row[5] else None
        user_id = row[8]  # El ID del usuario
        username = operaciones_BD.get_username_by_ticket(user_id)  # Obtener el nombre del usuario

        ticket = {
            'id': row[0],
            'titulo': row[1],
            'descripcion': row[2],
            'estado': row[3],
            'turno': row[4],
            'fecha': fecha,  # Aquí la fecha ya es un objeto datetime
            'area': row[6],
            'celda': row[7],
            'username': username,  # Añadir el nombre del usuario
            'tecnico_id': row[9],
            'tipo_servicio': row[10]
        }
        tickets.append(ticket)

    conn.close()

    # Aquí chequeamos el rol del usuario autenticado
    user_role = current_user.role

    # Si el rol es "administrador" o "soporte", redirigir a su propia vista
    if user_role == 'administrador':
        return render_template('view_administrador/index.html', tickets=tickets)
    elif user_role == 'soporte':
        return render_template('view_soporte/index.html', tickets=tickets)
    elif user_role == 'produccion':
        return render_template('view_produccion/index.html', tickets=tickets)

    # Si no coincide con ningún rol específico, redirigir a una página por defecto
    return render_template('index.html', tickets=tickets)

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    logout_user()  # Cierra la sesión del usuario
    return redirect(url_for('login'))  # Redirige a la página de login


@app.route('/usuarios')
@login_required  
def usuarios():
    return render_template('usuarios.html')

@app.route('/tickets')
@login_required  
def tickets():
    return render_template('tickets.html')

#consultas de bd ( para desarrollo)
@app.route('/get_users', methods=['GET'])
def get_users():
    users = operaciones_BD.get_list_users()
    return {'users': users}

@app.route('/get_name/<int:user_id>', methods=['GET'])
def get_name(user_id):
    user = operaciones_BD.get_username_by_ticket(user_id)
    return {'user': user}

@app.route('/get_tickets', methods=['GET'])
def get_tickets():
    tickets = operaciones_BD.get_list_tickets()
    return {'tickets': tickets}

@app.route('/get_ticket/<int:ticket_id>', methods=['GET'])
def get_info_ticket(ticket_id):
    ticket = operaciones_BD.get_info_ticket(ticket_id)
    if ticket is None:
        return {'error': 'Ticket not found'}, 404
    return {'ticket': ticket}

@app.route('/get_user/<int:user_id>', methods=['GET'])
def get_info_user(user_id):
    user = operaciones_BD.get_info_user(user_id)
    if user is None:
        return {'error': 'User not found'}, 404
    return {'user': user}

# Operaciones CRUD de usuarios ( produccion )
@app.route('/append_user/<username>/<password>', methods=['GET', 'POST'])
@login_required  
def append_user(username, password):
    if request.method == 'POST':
        operaciones_BD.register_user(username, password, 'user')
        return 'Usuario agregado con éxito'
    elif request.method == 'GET':
        return f"Recibido GET. Usuario: {username}, Contraseña: {password}"


#operaciones CRUD de tickets
@app.route('/append_ticket/<titulo>/<descripcion>/<estado>/<usuario_id>', methods=['GET', 'POST'])
@login_required 
def append_ticket(titulo, descripcion, estado, usuario_id):
    if request.method == 'POST':
        operaciones_BD.register_ticket(titulo, descripcion, estado, usuario_id)
        return 'Ticket agregado con éxito'
    elif request.method == 'GET': # cambiar por Get y viceversa
        return f"Recibido POST. Título: {titulo}, Descripción: {descripcion}, Estado: {estado}, ID del Usuario: {usuario_id}"
    
    return redirect(url_for('index'))

@app.route('/update_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required  
def update_ticket(ticket_id):
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            print(ticket_id)
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            estado = request.form['estado']
            usuario_id = request.form['usuario_id']
            
            # Asegúrate de que los valores sean correctos y no nulos
            if not titulo or not descripcion or not estado or not usuario_id:
                return "Todos los campos deben estar completos", 400
            
            # Actualizar el ticket en la base de datos
            operaciones_BD.update_ticket(ticket_id, titulo, descripcion, estado, usuario_id)
            
            # Redirigir de nuevo al index después de actualizar
            return redirect(url_for('index'))

        except KeyError as e:
            # Si falta alguna clave en el formulario, capturamos el error
            return f"Falta un campo en el formulario: {e}", 400
        except Exception as e:
            # Capturar otros errores generales
            return f"Error inesperado: {e}", 500
    else:
        # Obtener el ticket actual de la base de datos usando su ID
        ticket = operaciones_BD.get_element_by_id('tickets', ticket_id)
        return render_template('update_ticket.html', ticket=ticket)

@app.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
@login_required  
def delete_ticket(ticket_id):
    # Eliminar el ticket de la base de datos
    operaciones_BD.delete_ticket(ticket_id)
    
    # Redirigir de nuevo al index después de eliminar
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
