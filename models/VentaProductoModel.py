from datetime import datetime
from flask import jsonify
from db import db, ma


class VentaProducto(db.Model):
    id_venta = db.Column(db.Integer, db.ForeignKey('categoria.id'), primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)


class VentaProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VentaProducto
        fields = ["id_producto", "id_venta"]


def registrar_venta_producto(id_producto, id_venta):
    venta_producto = VentaProducto(id_producto = id_producto, id_venta = id_venta)
    db.session.add(venta_producto)
    if db.session.commit():
        venta_producto_schema = VentaProductoSchema()
        return venta_producto_schema.dump(venta_producto)
    return None

