from datetime import datetime
from flask import jsonify
from db import db, ma
from werkzeug.security import generate_password_hash


class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_compra = db.Column(db.Date, nullable=True)
    valor_total = db.Column(db.Double, nullable=False)
    estado = db.Column(db.String(1), default='C') #C - Carrito, V - Vendida
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class VentaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Venta
        fields = ["id", "fecha_compra", "valor_total", "estado"]


def crear_venta(id_cliente):
    venta = Venta(valor_total = 0, id_cliente = id_cliente)
    db.session.add(venta)
    db.session.commit()
    venta_schema = VentaSchema()
    return venta_schema.dump(venta)
    # return None

def consultar_venta_carrito(id_cliente):
    venta = Venta.query.filter_by(id_cliente = id_cliente, estado = 'C').first()
    if venta != None:
        venta_schema = VentaSchema()
        return venta_schema.dump(venta)
    return None

