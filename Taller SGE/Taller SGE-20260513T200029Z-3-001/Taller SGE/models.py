from extensions import db
from datetime import datetime
from flask_login import UserMixin

class Usuarios(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password_hash = db.Column(db.String(255))
    rol = db.Column(db.String(20))
    bio = db.Column(db.String(500))

class Eventos(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.String(500))
    fecha = db.Column(db.Date)
    capacidad = db.Column(db.Integer)
    categoria = db.Column(db.String(100))
    organizador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

class Registracion(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'))
    fecha = db.Column(db.DateTime)
    usuarios = db.relationship('Usuarios', backref='inscripciones')
    eventos = db.relationship('Eventos', backref='inscripciones')
    
