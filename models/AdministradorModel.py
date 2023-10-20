from datetime import datetime
from flask import jsonify
from db import db, ma
from werkzeug.security import generate_password_hash, check_password_hash


class Administrador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class AdministradorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Administrador
        fields = ["id", "nombre", "correo", "password"]


def registrar_administrador(nombre, correo, direccion, password):
    administrador = Administrador(nombre = nombre, correo = correo, password= generate_password_hash(password))
    db.session.add(administrador)
    db.session.commit()    
    cliente_schema = AdministradorSchema()
    return cliente_schema.dump(administrador)

def login_administrador(correo, password):
    administrador = Administrador.query.filter_by(correo=correo).first()
    if administrador != None:
        if check_password_hash(administrador.password, password):
            administrador_schema = AdministradorSchema()
            return administrador_schema.dump(administrador)
    return None