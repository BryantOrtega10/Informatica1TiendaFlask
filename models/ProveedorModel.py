from datetime import datetime
from flask import jsonify
from db import db, ma
from werkzeug.security import generate_password_hash


class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class ProveedorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Proveedor
        fields = ["id", "nombre", "correo", "direccion"]


def obtener_proveedores():
    proveedores_qs = Proveedor.query.all()
    proveedor_schema = ProveedorSchema()
    proveedores = [proveedor_schema.dump(proveedor) for proveedor in proveedores_qs]
    return proveedores

def obtener_provedor(id):
    proveedor = proveedor.query.filter.by(id=id)
    if proveedor != None:
        return proveedor
    return None

def registrar_proveedor(nombre, correo, direccion):
    proveedor = Proveedor(nombre = nombre, correo = correo,direccion = direccion)
    db.session.add(proveedor)
    if db.session.commit():
        proveedor_schema = ProveedorSchema()
        return proveedor_schema.dump(proveedor)
    return None


def modificar_proveedor(id, nombre, correo, direccion):
    proveedor = Proveedor.query.filter_by(id=id).first()
    if proveedor != None:
        proveedor.nombre = nombre
        proveedor.correo = correo
        proveedor.direccion = direccion
        if db.session.commit():
            proveedor_schema = ProveedorSchema()
            return proveedor_schema.dump(proveedor)
    return None


def eliminar_proveedor(id):
    Proveedor.delete().where(Proveedor.c.id == id)
    if db.session.commit():
        return True       
    return None