from flask import Flask, render_template,request, redirect, url_for
from tools import operaciones_BD
app = Flask(__name__)

# Dummy user data (for demonstration purposes)
USER_CREDENTIALS = {
    'admin': 'password123'
}
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Aquí deberías verificar el usuario y la contraseña
        if username == 'admin' and password == 'admin':  # Esto es solo un ejemplo
            return redirect(url_for('index'))  # Redirige a la página principal si el login es exitoso
        else:
            error_message = 'Usuario o contraseña incorrectos'  # Mensaje de error
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')

@app.route('/index')
def index():
    # Obtener la lista de tickets desde la base de datos
    tickets = operaciones_BD.get_list_tickets()
    
    # Pasar la lista de tickets a la plantilla index.html
    return render_template('index.html', tickets=tickets)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

#operaciones CRUD de usuarios
@app.route('/get_users', methods=['GET'])
def get_users():
    users = operaciones_BD.get_list_users()
    return {'users': users}

@app.route('/append_user/<username>/<password>', methods=['GET', 'POST'])
def append_user(username, password):
    if request.method == 'POST':
        operaciones_BD.register_user(username, password, 'user')
        return 'Usuario agregado con éxito'
    elif request.method == 'GET':
        return f"Recibido GET. Usuario: {username}, Contraseña: {password}"

#operaciones CRUD de tickets
@app.route('/get_tickets', methods=['GET'])
def get_tickets():
    tickets = operaciones_BD.get_list_tickets()
    return {'tickets': tickets}

@app.route('/update_ticket/<ticket_id>/<titulo>/<descripcion>/<estado>/<usuario_id>', methods=['GET', 'POST'])
def update_ticket(ticket_id, titulo, descripcion, estado, usuario_id):
    if request.method == 'POST':
        operaciones_BD.update_ticket(ticket_id, titulo, descripcion, estado, usuario_id)
        return 'Ticket actualizado con éxito'
    elif request.method == 'GET':
        return f"Recibido GET. Ticket ID: {ticket_id}, Título: {titulo}, Descripción: {descripcion}, Estado: {estado}, Usuario ID: {usuario_id}"

@app.route('/delete_ticket/<ticket_id>', methods=['GET', 'POST'])
def delete_ticket(ticket_id):
    if request.method == 'POST':
        operaciones_BD.delete_ticket(ticket_id)
        return 'Ticket eliminado con éxito'
    elif request.method == 'GET':
        return f"Recibido GET. Ticket ID: {ticket_id}"


if __name__ == '__main__':
    app.run(debug=True)
