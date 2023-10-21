from http import HTTPStatus
from flask import Blueprint, jsonify, session, Response, request, render_template, redirect, url_for
from models.ClienteModel import cliente_login, registrar_cliente, vertificar_existencia_cliente


clientes = Blueprint("clientes", __name__, url_prefix="/clientes")

@clientes.route("/loggout", methods=["GET"])
def loggout():
    del session['correo'];
    del session['id'];
    return redirect(url_for('tienda.inicio'))

@clientes.route("/login", methods=["GET", "POST"])
def login():
    if 'correo' in session:
        return redirect(url_for('tienda.inicio'))
    
    if request.method == "POST":
        if 'correo' not in request.form or len(request.form.get('correo').strip()) == 0:
            return jsonify({"success": False, "error" : "Campo correo vacio"}) , HTTPStatus.BAD_REQUEST
        
        if 'contrasena' not in request.form or len(request.form.get('contrasena').strip()) == 0:
            return jsonify({"success": False, "error" : "Campo password vacio"}) , HTTPStatus.BAD_REQUEST
        
        req_correo = request.form.get('correo')
        req_contrasena = request.form.get('contrasena')
        clienteLoggedo = cliente_login(req_correo, req_contrasena)
        if clienteLoggedo is None:
            return jsonify({"success": False, "error" : "Usuario o contraseña incorrectos"}) , HTTPStatus.BAD_REQUEST
        
        session['correo'] = req_correo
        session['id'] = clienteLoggedo["id"]
        return jsonify({"success": True, "message" : "Bienvenido!"}), HTTPStatus.OK

    return render_template("login.html")


@clientes.route("/registrarme", methods=["GET", "POST"])
def registrarme():
    if 'correo' in session:
        return redirect(url_for('tienda.inicio'))
    
    if request.method == "POST":
        if 'nombre' not in request.form or len(request.form.get('nombre').strip()) == 0:
            return jsonify({"success": False, "error" : "Campo nombre vacio"}) , HTTPStatus.BAD_REQUEST
        
        if 'direccion' not in request.form or len(request.form.get('direccion').strip()) == 0:
            return jsonify({"success": False, "error" : "Campo direccion vacio"}) , HTTPStatus.BAD_REQUEST
        
        if 'correo' not in request.form or len(request.form.get('correo').strip()) == 0:
            return jsonify({"success": False, "error" : "Campo correo vacio"}) , HTTPStatus.BAD_REQUEST
        
        if 'contrasena' not in request.form or len(request.form.get('contrasena').strip()) == 0:
            return jsonify({"success": False, "error" : "Campo contrasena vacio"}) , HTTPStatus.BAD_REQUEST
        
        if 'r_contrasena' not in request.form or len(request.form.get('contrasena').strip()) == 0:
            return jsonify({"success": False, "error" : "Campo repita la contrasena vacio"}) , HTTPStatus.BAD_REQUEST
        

        req_correo = request.form.get('correo')
        req_contrasena = request.form.get('contrasena')
        req_nombre = request.form.get('nombre')
        req_direccion = request.form.get('direccion')
        req_r_contrasena = request.form.get('r_contrasena')

        if req_r_contrasena != req_contrasena:
            return jsonify({"success": False, "error" : "Las contraseñas no coinciden"}) , HTTPStatus.BAD_REQUEST

        if vertificar_existencia_cliente(req_correo):
            return jsonify({"success": False, "error" : "El correo ya esta registrado"}) , HTTPStatus.BAD_REQUEST


        registroCliente = registrar_cliente(req_nombre, req_correo, req_direccion, req_contrasena)
        if registroCliente is None:
            return jsonify({"success": False, "error" : "Error al registrar al cliente"}) , HTTPStatus.BAD_REQUEST
        
        session['correo'] = req_correo
        session['id'] = registroCliente["id"]
        return jsonify({"success": True, "message" : "Bienvenido!"}), HTTPStatus.OK

    return render_template("registrarme.html")