from http import HTTPStatus
from flask import Blueprint, jsonify, session, Response, request, render_template, redirect, url_for
from models.CategoriaModel import consultar_categorias, categoria_x_id
from models.ProductoModel import producto_x_categoria, producto_x_id

tienda = Blueprint("tienda", __name__, url_prefix="/")

@tienda.route("/", methods=["GET"])
def inicio():
    categorias = consultar_categorias()
    productos_x_categoria = []
    for categoria in categorias:
        productos_x_categoria.append({"categoria": categoria, "productos": producto_x_categoria(categoria["id"])})
    
    return render_template("index.html", productos_x_categoria = productos_x_categoria)


@tienda.route("/<id_categoria>", methods=["GET"])
def ver_prod_x_categoria(id_categoria):
    categoria = categoria_x_id(id_categoria)
    productos = producto_x_categoria(id_categoria)
    return render_template("productos_x_categoria.html", productos = productos, categoria = categoria)

@tienda.route("/producto/<id_producto>", methods=["GET"])
def ver_producto(id_producto):
    
    producto = producto_x_id(id_producto)
    categoria = categoria_x_id(producto["id_categoria"])
    return render_template("producto.html", producto = producto, categoria = categoria)
