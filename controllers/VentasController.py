from http import HTTPStatus
from flask import Blueprint, flash, session, Response, request, render_template, redirect, url_for

from models.VentaModel import consultar_venta_carrito, crear_venta, cambiar_estado_venta
from models.VentaProductoModel import agregar_cantidad, modificar_cantidad, quitar_producto, traer_productos_carrito
from models.ProductoModel import producto_x_id, restar_stock


ventas = Blueprint("ventas", __name__, url_prefix="/carrito")
@ventas.route("/agregar-productos", methods=["POST"])
def agregar_productos():
    if 'idproducto' not in request.form or len(request.form.get('idproducto').strip()) == 0:
        flash('el id de producto esta vacio')
        return redirect(request.referrer)

    if 'cantidad' not in request.form or len(request.form.get('cantidad').strip()) == 0 or int(request.form.get('cantidad')) <= 0:
        flash('Cantidad vacia')
        return redirect(request.referrer)
 
    req_idproducto = request.form.get('idproducto')
    req_cantidad = request.form.get('cantidad')

    producto = producto_x_id(req_idproducto)
    if producto["stock"] < int(req_cantidad):
        flash('No hay stock suficiente de este producto')
        return redirect(request.referrer)
    

    # Consultar si hay "ventas" con estado C si no crea una
    carrito = consultar_venta_carrito(session['id'])
    if carrito is None:
        carrito = crear_venta(session['id'])
        
    # Consultar si hay una VentaProducto para este producto
    agrego_cantidad = agregar_cantidad(req_idproducto, carrito["id"], req_cantidad)
    if agrego_cantidad == False:
        flash('Error desconocido')
        return redirect(request.referrer)
    
    return redirect(url_for('ventas.carrito'))


@ventas.route("/modificar-productos", methods=["POST"])
def modificar_productos():
    if 'idproducto' not in request.form or len(request.form.get('idproducto').strip()) == 0:
        flash('el id de producto esta vacio')
        return redirect(request.referrer)

    if 'cantidad' not in request.form or len(request.form.get('cantidad').strip()) == 0 or int(request.form.get('cantidad')) <= 0:
        flash('Cantidad vacia')
        return redirect(request.referrer)
 
    req_idproducto = request.form.get('idproducto')
    req_cantidad = request.form.get('cantidad')

    producto = producto_x_id(req_idproducto)
    if producto["stock"] < int(req_cantidad):
        flash('No hay stock suficiente de este producto')
        return redirect(request.referrer)
    

    # Consultar si hay "ventas" con estado C si no crea una
    carrito = consultar_venta_carrito(session['id'])
    if carrito is None:
        carrito = crear_venta(session['id'])
        
    # Consultar si hay una VentaProducto para este producto
    agrego_cantidad = modificar_cantidad(req_idproducto, carrito["id"], req_cantidad)
    if agrego_cantidad == False:
        flash('Error desconocido')
        return redirect(request.referrer)
    
    return redirect(url_for('ventas.carrito'))


@ventas.route("/quitar-producto", methods=["POST"])
def quitar_productos():
    if 'idproducto' not in request.form or len(request.form.get('idproducto').strip()) == 0:
        flash('el id de producto esta vacio')
        return redirect(request.referrer)

    req_idproducto = request.form.get('idproducto')

    # Consultar si hay "ventas" con estado C si no crea una
    carrito = consultar_venta_carrito(session['id'])
    if carrito is None:
        carrito = crear_venta(session['id'])
        
    
    quito_cantidad = quitar_producto(req_idproducto, carrito["id"])
    if quito_cantidad == False:
        flash('Error desconocido')
        return redirect(request.referrer)
    
    return redirect(url_for('ventas.carrito'))



@ventas.route("/", methods=["GET"])
def carrito():
    if 'id' not in session:
        return redirect(url_for('tienda.inicio'))

    carrito = consultar_venta_carrito(session['id'])
    
    if carrito is None:
        return redirect(url_for('tienda.inicio'))
    
    items = traer_productos_carrito(carrito['id'])
    subtotal = 0
    for (i,item) in enumerate(items):
        items[i]["producto"] = producto_x_id(item["id_producto"])
        subtotal += item["cantidad"] * items[i]["producto"]["precio"]
    
    return render_template("carrito.html", items = items, carrito = carrito, subtotal=subtotal)    


@ventas.route("/comprar", methods=["POST"])
def comprar():
    if 'id' not in session:
        return redirect(url_for('tienda.inicio'))

    carrito = consultar_venta_carrito(session['id'])
    
    if carrito is None:
        return redirect(url_for('tienda.inicio'))
    
    items = traer_productos_carrito(carrito['id'])
    if len(items) == 0:
        return redirect(url_for('tienda.inicio'))
    

    if cambiar_estado_venta(carrito["id"]):
        for item in items:
            restar_stock(item["id_producto"], item["cantidad"])

        return redirect(url_for('ventas.gracias'))
    else:
        flash('Error al comprar')
        return redirect(request.referrer)


@ventas.route("/gracias", methods=["GET"])
def gracias():
    return render_template("gracias.html")    
