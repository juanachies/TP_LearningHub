# python -m venv entorno_virtual -> creo entorno virtual
# entorno_virtual/Scripts/activate  -> activo entorno virtual
# pip install flask 
# pip install flask_sqlalchemy

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

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
    comentario = db.Column(db.Text)

    def __repr__(self):
        return f"Apunte: {self.apunte}"

with app.app_context():
    db.create_all() #creo las tablas



UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/comunidad', methods=['GET', 'POST'])
def comunidad():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        carrera = request.form['carrera']
        comentario = request.form.get('comentario', '')
        archivo = request.files['archivo']

        if not archivo or not archivo.filename.endswith('.pdf'):
            return redirect(url_for('comunidad'))

        nombre_archivo = archivo.filename
        ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
        archivo.save(ruta_archivo)

        # Crear usuario (si no existe ese email)
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            usuario = Usuario(nombre_completo=nombre, email=email, telefono=telefono)
            db.session.add(usuario)
            db.session.commit()

        # Crear apunte
        nuevo_apunte = Apunte(
            id_usuario=usuario.id,
            carrera=carrera,
            apunte=nombre_archivo,
            comentario=comentario
        )
        db.session.add(nuevo_apunte)
        db.session.commit()

        return redirect(url_for('comunidad'))

    return render_template('0104.comunidad.html')



if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 8000)
