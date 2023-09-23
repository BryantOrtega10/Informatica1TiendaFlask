from datetime import datetime
from flask import jsonify
from db import db, ma


class ProductoCategoria(db.Model):
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), primary_key=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), primary_key=True)


class ProductoCategoriaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductoCategoria
        fields = ["id_producto", "id_categoria"]


def registrar_producto_categoria(id_producto, id_categoria):
    producto_categoria = ProductoCategoria(id_producto = id_producto, id_categoria = id_categoria)
    db.session.add(producto_categoria)
    if db.session.commit():
        producto_categoria_schema = ProductoCategoriaSchema()
        return producto_categoria_schema.dump(producto_categoria)
    return None

