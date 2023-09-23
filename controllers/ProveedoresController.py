from models.ProveedorModel import obtener_proveedores, obtener_provedor

from http import HTTPStatus
from flask import Blueprint, Response, request, render_template, flash


proveedores = Blueprint("proveedores", __name__, url_prefix="/proveedores")

@proveedores.route("/lista-proveedores")
def mostrar_proveedores():
    proveedores = obtener_proveedores()
    return render_template("proveedores.html", proveedores=proveedores)

@proveedores.route("/<int:id>")
def obtener_proveedor(id):
    proveedor = obtener_provedor(id)
