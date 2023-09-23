from datetime import datetime
from flask import jsonify
from db import db, ma


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)


class CategoriaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        fields = ["id", "nombre"]


def registrar_categoria(nombre):
    cliente = Categoria(nombre = nombre)
    db.session.add(cliente)
    if db.session.commit():
        cliente_schema = CategoriaSchema()
        return cliente_schema.dump(cliente)
    return None

