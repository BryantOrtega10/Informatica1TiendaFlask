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
    categoria = Categoria(nombre = nombre)
    db.session.add(categoria)
    if db.session.commit():
        categoria_schema = CategoriaSchema()
        return categoria_schema.dump(categoria)
    return None

def consultar_categorias():
    
    categorias = Categoria.query.all()
    categoria_schema = CategoriaSchema()
    categorias_res = [categoria_schema.dump(categoria) for categoria in categorias]
    return categorias_res

def categoria_x_id(id_categoria):    
    categoria = Categoria.query.filter_by(id = id_categoria).first()
    categoria_schema = CategoriaSchema()
    categoria_res = categoria_schema.dump(categoria)
    return categoria_res