from datetime import datetime
from flask import jsonify
from db import db, ma
from werkzeug.security import generate_password_hash


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Double, nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class ProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        fields = ["id", "nombre", "imagen", "precio", "descripcion"]


def registrar_producto(nombre, imagen, precio, descripcion):
    producto = Producto(nombre = nombre, imagen = imagen,precio = precio, descripcion=descripcion)
    db.session.add(producto)
    if db.session.commit():
        producto_schema = ProductoSchema()
        return producto_schema.dump(producto)
    return None


def modificar_producto(id, nombre, imagen, precio, descripcion):
    producto = Producto.query.filter_by(id=id).first()
    if producto != None:
        producto.nombre = nombre
        producto.imagen = imagen
        producto.precio = precio
        producto.descripcion = descripcion
        if db.session.commit():
            producto_schema = ProductoSchema()
            return producto_schema.dump(producto)
    return None


def eliminar_producto(id):
    Producto.delete().where(Producto.c.id == id)
    if db.session.commit():
        return True       
    return None


def producto_login(correo, password):
    producto = Producto.query.filter_by(correo=correo,password = generate_password_hash(password, method="sha256")).first()
    if producto != None:
        return producto
    return None