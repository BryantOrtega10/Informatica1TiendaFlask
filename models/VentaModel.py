from datetime import datetime
from flask import jsonify
from db import db, ma
from werkzeug.security import generate_password_hash


class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    valor_total = db.Column(db.Double, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class VentaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Venta
        fields = ["id", "fecha", "valor_total"]


def registrar_venta(fecha, valor_total):
    venta = Venta(fecha = fecha)
    db.session.add(venta)
    if db.session.commit():
        venta_schema = VentaSchema()
        return venta_schema.dump(venta)
    return None


def modificar_venta(id, fecha, valor_total):
    venta = Venta.query.filter_by(id=id).first()
    if venta != None:
        venta.nombre = nombre
        venta.correo = correo
        venta.direccion = direccion
        if db.session.commit():
            venta_schema = VentaSchema()
            return venta_schema.dump(venta)
    return None


def eliminar_venta(id):
    Venta.delete().where(Venta.c.id == id)
    if db.session.commit():
        return True       
    return None