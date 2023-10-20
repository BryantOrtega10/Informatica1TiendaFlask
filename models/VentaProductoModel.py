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


def agregar_cantidad(id_producto, id_venta, cantidad):
    venta_producto = VentaProducto.query.filter_by(id_producto = id_producto, id_venta = id_venta).first()
    if venta_producto != None:
        venta_producto.cantidad += cantidad        
    else:
        venta_producto = VentaProducto(id_producto = id_producto, id_venta = id_venta, cantidad = cantidad)
        db.session.add(venta_producto)

    db.session.commit()
    return True
    

