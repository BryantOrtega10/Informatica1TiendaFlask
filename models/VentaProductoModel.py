from datetime import datetime
from flask import jsonify
from db import db, ma


class VentaProducto(db.Model):
    id_venta = db.Column(db.Integer, db.ForeignKey('venta.id'), primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)


class VentaProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VentaProducto
        fields = ["id_producto", "id_venta","cantidad"]


def agregar_cantidad(id_producto, id_venta, cantidad):
    venta_producto = VentaProducto.query.filter_by(id_producto = id_producto, id_venta = id_venta).first()
    if venta_producto != None:
        venta_producto.cantidad += int(cantidad)
    else:
        venta_producto = VentaProducto(id_producto = id_producto, id_venta = id_venta, cantidad = cantidad)
        db.session.add(venta_producto)

    db.session.commit()
    return True


def modificar_cantidad(id_producto, id_venta, cantidad):
    venta_producto = VentaProducto.query.filter_by(id_producto = id_producto, id_venta = id_venta).first()
    if venta_producto != None:
        venta_producto.cantidad = int(cantidad)
    else:
        venta_producto = VentaProducto(id_producto = id_producto, id_venta = id_venta, cantidad = cantidad)
        db.session.add(venta_producto)

    db.session.commit()
    return True


def traer_productos_carrito(id_venta):
    venta_productos = VentaProducto.query.filter_by(id_venta = id_venta).all()
    venta_prod_schema = VentaProductoSchema()

    return [venta_prod_schema.dump(venta_producto) for venta_producto in venta_productos]  



def quitar_producto(id_producto, id_venta):
    VentaProducto.query.filter(VentaProducto.id_producto == id_producto, VentaProducto.id_venta == id_venta).delete()
    if db.session.commit():
        return True       
    return False   

