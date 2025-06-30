# python -m venv entorno_virtual -> creo entorno virtual
# entorno_virtual/Scripts/activate  -> activo entorno virtual
# pip install flask 
# pip install flask_sqlalchemy

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base_de_datos.db'
db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    telefono = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Usuario: {self.nombre_completo}"
    

class Apunte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    carrera = db.Column(db.String(30), nullable=False)
    apunte = db.Column(db.String(100), nullable=False)
    ruta = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)

    usuario = db.relationship('Usuario', backref='apuntes')

    def __repr__(self):
        return f"Apunte: {self.apunte}"

with app.app_context():
    db.create_all() #creo las tablas


# Rutas a los distintos archivos con flask

@app.route('/')
def index():
    return render_template('0101.index.html')

@app.route('/informacion')
def informacion():
    return render_template('0102.informacion.html')

@app.route('/descargar')
def descargar():
    return render_template('0103.descarga.html')


@app.route('/comunidad', methods =['GET', 'POST'])
def comunidad():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        carrera = request.form['carrera']

        archivo = request.files['archivo']
        nombre_archivo = archivo.filename

        descripcion = request.form['descripcion']
    
        archivo.save(f'uploads/{carrera}/{nombre_archivo}')
    
        #Creo usuario y apunte
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            usuario = Usuario(
                nombre_completo = nombre,
                email = email,
                telefono = telefono
            )
            db.session.add(usuario)
            db.session.commit()

        apunte = Apunte(
            id_usuario = usuario.id,
            carrera = carrera,
            apunte = nombre_archivo, 
            ruta = f'/uploads/{carrera}/{nombre_archivo}', 
            descripcion = descripcion
        )
        db.session.add(apunte)
        db.session.commit()

        return redirect(url_for('apuntes'))

    return render_template('0104.comunidad.html')


@app.route('/apuntes')
def apuntes():
    apuntes = Apunte.query.all()
    apuntes_por_carrera = {}
    for apunte in apuntes:
        carrera = apunte.carrera
        if carrera not in apuntes_por_carrera:
            apuntes_por_carrera[carrera] = []
        apuntes_por_carrera[carrera].append(apunte)

    return render_template('0105.apuntes.html', apuntes_por_carrera=apuntes_por_carrera)


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 8000)