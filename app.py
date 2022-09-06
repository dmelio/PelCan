from flask import Flask, render_template, request, redirect , url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbmascotas'
mysql = MySQL(app)

app.secret_key='mysecretkey'

@app.route('/')
def Index():
    return render_template('index.html')

@app.route ('/admin_usuarios')
def adm_usuarios():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario')
    data = cur.fetchall()
    return render_template('adm-usuarios.html', usuarios = data)

@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
       Nombre = request.form['Nombre']
       telefono = request.form['telefono']
       email = request.form['email']
       direccion = request.form['direccion']
       password = request.form['password']
       cur = mysql.connection.cursor()
       cur.execute('INSERT INTO usuario (nombre, telefono, email, direccion, password) VALUES(%s, %s, %s, %s, %s)',
       (Nombre, telefono, email, direccion, password))
       mysql.connection.commit()
       flash('Usuario guardado con exito')
       return redirect(url_for('Index'))


@app.route('/add_venta')
def add_venta():
    return 'generar venta'


@app.route('/add_servicio')
def add_servicio():
    return 'agregar servicio'
    
@app.route ('/edit_usuario/<id>')
def get_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario WHERE id = %s',(id))
    data = cur.fetchall()
    return render_template('edit-usuario.html', usuario = data[0])

@app.route ('/update/<id>', methods = ['POST'])
def update_usuario(id):
    if request.method == 'POST':
        nombre = request.form['Nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        direccion = request.form['direccion']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE usuario 
            SET nombre = %s,
            telefono = %s,
            email = %s,
            direccion = %s,
            password = %s
        WHERE id = %s
    """, (nombre,telefono,email,direccion,password,id))
        mysql.connection.commit()
        flash('Usuario actualizado')
        return redirect(url_for('Index'))


@app.route ('/delete_usuario/<string:id>')
def delete_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuario WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Usuario eliminado con exito')
    return redirect(url_for('Index'))

@app.route ('/edit_servicio')
def edit_servicio():
    return 'editar servicio'

@app.route ('/delete_servicio')
def delete_servicio():
    return 'eliminar servicio'

if __name__ == '__main__':
    app.run(port = 3000, debug = True)