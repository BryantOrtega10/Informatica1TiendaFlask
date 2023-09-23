from datetime import datetime
from flask import jsonify
from db import db, ma
from werkzeug.security import generate_password_hash


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        fields = ["id", "nombre", "correo", "direccion", "password"]


def registrar_cliente(nombre, correo, direccion, password):
    cliente = Cliente(nombre = nombre, correo = correo,direccion = direccion, password= generate_password_hash(password, method="sha256"))
    db.session.add(cliente)
    if db.session.commit():
        cliente_schema = ClienteSchema()
        return cliente_schema.dump(cliente)
    return None


def modificar_cliente(id, nombre, correo, direccion):
    cliente = Cliente.query.filter_by(id=id).first()
    if cliente != None:
        cliente.nombre = nombre
        cliente.correo = correo
        cliente.direccion = direccion
        if db.session.commit():
            cliente_schema = ClienteSchema()
            return cliente_schema.dump(cliente)
    return None


def eliminar_cliente(id):
    Cliente.delete().where(Cliente.c.id == id)
    if db.session.commit():
        return True       
    return None


def cliente_login(correo, password):
    cliente = Cliente.query.filter_by(correo=correo,password = generate_password_hash(password, method="sha256")).first()
    if cliente != None:
        return cliente
    return None