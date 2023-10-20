from http import HTTPStatus
from flask import Blueprint, flash, session, Response, request, render_template, redirect, url_for

from models.VentaModel import consultar_venta_carrito, crear_venta
from models.VentaProductoModel import agregar_cantidad


ventas = Blueprint("ventas", __name__, url_prefix="/carrito")

@ventas.route("/agregar-productos", methods=["POST"])
def agregar_productos():
    if 'idproducto' not in request.form or len(request.form.get('idproducto').strip()) == 0:
        flash('el id de producto esta vacio')
        return redirect(request.referrer)

    if 'cantidad' not in request.form or len(request.form.get('cantidad').strip()) == 0 or int(request.form.get('cantidad')) <= 0:
        flash('Cantidad vacia')
        return redirect(request.referrer)
 
    # Consultar si hay "ventas" con estado C si no crea una
    carrito = consultar_venta_carrito(session['id'])
    if carrito is None:
        carrito = crear_venta(session['id'])

    req_idproducto = request.form.get('idproducto')
    req_cantidad = request.form.get('cantidad')


    # Consultar si hay una VentaProducto para este producto
    agrego_cantidad = agregar_cantidad(req_idproducto, carrito["id"], req_cantidad)
    if agrego_cantidad == False:
        flash('Error desconocido')
        return redirect(request.referrer)
    
    return redirect(url_for('tienda.inicio'))

