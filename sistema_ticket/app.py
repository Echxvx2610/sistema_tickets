from flask import Flask, render_template,request, redirect, url_for

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
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
